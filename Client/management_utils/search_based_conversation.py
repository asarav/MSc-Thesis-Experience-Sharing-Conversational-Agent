from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from chatterbot import comparisons
from chatterbot import response_selection
import management_utils.cosine_similarity as cosine

import spacy


class SearchBasedConversation:
    def __init__(self, conversations, chatbotName):        
        self.nlp = spacy.load('en_core_web_md')
        self.chatbot = ChatBot(chatbotName,
                logic_adapters=[
                    {
                        "import_path": "chatterbot.logic.BestMatch",
                        "statement_comparison_function": comparisons.LevenshteinDistance,
                        "response_selection_method": response_selection.get_first_response
                    }
                ])

        self.conversations = conversations

        self.answered = [False] * len(self.conversations)

        self.trainer = ListTrainer(self.chatbot)

        # Train each conversation 3 times
        for conversation in self.conversations:
            for i in range(3):
                self.trainer.train(conversation)


    def askQuestion(self, question):
        print(question)

        response = self.chatbot.get_response(question)
        print(response.confidence)
        print(response)

        #Try TF-IDF
        similarities = []
        cosineSimilarities = []
        questionDoc = self.nlp(question)
        maxQuestionIndex = 0
        maxQuestion = 0
        maxAnswerIndex = 0
        maxAnswer = 0

        for item in range(len(self.conversations)):
            conversation = self.conversations[item]
            questDoc = self.nlp(conversation[0])
            answerDoc = self.nlp(conversation[1])
            sims = [questDoc.similarity(questionDoc), answerDoc.similarity(questionDoc)]
            if sims[0] > maxQuestion:
                maxQuestion = sims[0]
                maxQuestionIndex = item
            if sims[1] > maxAnswer:
                maxAnswer = sims[1]
                maxAnswerIndex = item
            similarities.append(sims)


        maxACIndex = 0
        maxAC = 0
        maxQCIndex = 0
        maxQC = 0
        for item in range(len(self.conversations)):
            conversation = self.conversations[item]
            sims = [cosine.get_similarity(question, conversation[0]), cosine.get_similarity(question, conversation[1])]
            if sims[0] > maxQC:
                maxQC = sims[0]
                maxQCIndex = item
            if sims[1] > maxAC:
                maxAC = sims[1]
                maxACIndex = item
            cosineSimilarities.append(sims)

        print(maxQuestion)
        print(self.conversations[maxQuestionIndex])
        print(maxAnswer)
        print(self.conversations[maxAnswerIndex])

#        print(maxQC)
#        print(self.conversations[maxQCIndex])
#        print(maxAC)
#        print(self.conversations[maxACIndex])

        answer = self.conversations[maxQuestionIndex]
        print(answer)

        if self.answered[maxQuestionIndex]:
            return "I may have already given this answer, but maybe it might be useful. " + answer[1]

        self.answered[maxQuestionIndex] = True

        if maxQuestion < 0.7:
            return "I'm not sure if this is the correct answer, but I'll try my best. " + answer[1]
        else:
            return answer[1]