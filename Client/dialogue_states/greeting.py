import management_utils.response_manager as ResponseManager
import management_utils.search_based_conversation as SBC

class Greeting:
    def __init__(self):
        self.responseUtils = ResponseManager.ResponseManager()
        self.DiabetesAnswers = SBC.SearchBasedConversation([], "Diabetes Questions")
        self.ID = "1234"
        self.username = ""
        self.IncorrectName = False
        self.firstTimeDiabetesQuestion = True
        self.states = [{
            "name": "AskUserID",
            "statement": "Hello there. I am Diet Bot. Before we start, do you already have a user id?",
            "response": self.AskUserIDResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "NoUserID",
            "statement": self.NoUserIDStatement,
            "response": self.NoUserIDResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "Wait",
            "statement": "Okay. Let me know when you are ready.",
            "response": "WaitQuestion",
            "stateType": "Statement"
        },
        {
            "name": "WaitQuestion",
            "statement": "Your ID is " + self.ID + ". Are you ready now?",
            "response": self.WaitQuestionResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "Start",
            "statement": "Great! Let's get started then.",
            "response": "Greeting",
            "stateType": "Statement",
            "gesture": "Nod"
        },
        {
            "name": "Greeting",
            "statement": "I am Diet Bot. I am a conversational agent whose purpose is to help those with type 2 diabetes or who are at risk of being diagnosed with type 2 diabetes manage their diet. To begin, let's get acquainted.",
            "response": "AskName",
            "stateType": "Statement"
        },
        {
            "name": "AskName",
            "statement": "What is your name?",
            "response": self.AskNameResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ConfirmName",
            "statement": self.ConfirmNameStatement,
            "response": self.ConfirmNameResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "IncorrectName",
            "statement": "Okay. Could you say your name again?",
            "response": self.IncorrectNameResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "IncorrectName2",
            "statement": "I'm sorry. I will try to get this right. Could you repeat your name slowly so that I can understand?",
            "response": self.IncorrectNameResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "GetStartedGreeting",
            "statement": self.GetStartedGreetingStatement,
            "response": "IntroduceProcesses",
            "stateType": "Statement"
        },
        {
            "name": "IntroduceProcesses",
            "statement": "To begin, I will be working with you to develop a positive diet related habit over the next three days that can help you manage or prevent type II diabetes more effectively.",
            "response": "ExplainTypeIIDiabetes",
            "stateType": "Statement"
        },
        {
            "name": "ExplainTypeIIDiabetes",
            "statement": "Type 2 diabetes is a condition that results in a high blood glucose level. Blood glucose is also known as blood sugar. Type 2 diabetes results in symptoms like increased thirst and tiredness. Long term effects can be more serious. Long term effects include, but are not limited to heart disease, strokes, and kidney failure. Needless to say, the effects of diabetes when left untreated are extremely serious.",
            "response": "ExplainTreatments",
            "stateType": "Statement"
        },
        {
            "name": "ExplainTreatments",
            "statement": "There are a variety of treatments for Type II diabetes, but two approaches that are under your control are that of diet management and exercise. I will be focusing on diet.",
            "response": "AnswerDiabetesQuestions",
            "stateType": "Statement"
        },
        {
            "name": "AnswerDiabetesQuestions",
            "statement": self.AnswerDiabetesQuestionsStatement,
            "response": self.AnswerDiabetesQuestionsResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "AskDiabetesQuestion",
            "statement": "What is your question?",
            "response": self.AskDiabetesQuestionResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "DiabetesAnswer",
            "statement": self.ProvideDiabetesAnswer,
            "response": "AnswerDiabetesQuestions",
            "stateType": "Statement"
        },
        {
            "name": "ListGoals",
            "statement": "There are three goals that you can choose. These are calorie restriction, sugar reduction and diet composition change. Before we choose a goal, I would like to ask you for a few personal details so that we can ensure that the goal that is chosen is appropriate for you.",
            "response": "ListGoals",
            "stateType": "Statement"
        }
        ]

    def AskUserIDResponse(self, response):
        #Process the response here.
        nextState = "NoUserID"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "NoUserID"
        else:
            nextState = "NoUserID"
        return [], nextState

    def NoUserIDStatement(self):
        self.ID = "1234"
        return "Okay. Welcome. Here is your new user Id. " + "Your Id is: " + self.ID + ". Make sure you write it down somewhere. You will need it for all of the sessions we will have together. Do you have your ID memorized and written down somewhere?"

    def NoUserIDResponse(self, response):
        nextState = "NoUserID"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "Wait"
        else:
            nextState = "Start"
        return [], nextState

    def WaitQuestionResponse(self, response):
        nextState = "WaitQuestion"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "WaitQuestion"
        else:
            nextState = "Start"
        return [], nextState

    def AskNameResponse(self, response):
        nextState = "ConfirmName"
        print(response)
        self.username = response
        return [], nextState

    def ConfirmNameStatement(self):
        return "Your name is " + self.username + ". Is that correct?"

    def ConfirmNameResponse(self, response):
        nextState = "GetStartedGreeting"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            if self.IncorrectName:
                nextState = "IncorrectName2"
            else:
                nextState = "IncorrectName"
        else:
            nextState = "GetStartedGreeting"
        return [], nextState

    def IncorrectNameResponse(self, response):
        nextState = "ConfirmName"
        self.IncorrectName = True
        self.username = response
        return [], nextState

    def GetStartedGreetingStatement(self):
        return "Great. Nice to meet you " + self.username + ". Let's start improving your diet"

    def AnswerDiabetesQuestionsResponse(self, response):
        nextState = "AskDiabetesQuestion"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "ListGoals"
        else:
            nextState = "AskDiabetesQuestion"
        return [], nextState

    def AnswerDiabetesQuestionsStatement(self):
        if not self.firstTimeDiabetesQuestion:
            return "Do you have any other questions?"
        else:
            self.firstTimeDiabetesQuestion = False
            return "Do you have any questions about Type 2 Diabetes So far?"

    def AskDiabetesQuestionResponse(self, response):
        nextState = "DiabetesAnswer"
        self.DiabetesQuestionAnswer = self.DiabetesAnswers.askQuestion(response)
        return [], nextState

    def ProvideDiabetesAnswer(self):
        return self.DiabetesQuestionAnswer