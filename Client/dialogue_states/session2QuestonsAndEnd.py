import management_utils.response_manager as ResponseManager
import management_utils.search_based_conversation as SBC
import data_retrieval.memoryManager as shortTermData
import management_utils.diabetesConversation as diabetesConversation

class Session2QuestionsAndEnd:
    def __init__(self):
        self.responseUtils = ResponseManager.ResponseManager()
        self.DiabetesAnswers = SBC.SearchBasedConversation(diabetesConversation.conversation, "Diabetes Questions")
        self.ID = "1234"
        self.username = ""
        self.firstTimeDiabetesQuestion = True
        self.gender = 0
        self.age = 18
        self.weight = 60
        self.height = 160

        #Load user data
        self.shortTermData = shortTermData.MemoryManager()
        self.shortTermData.data["session"] = 1

        self.states = [
        {
            "name": "AskStruggle",
            "statement": self.AskStruggleStatement,
            "response": self.AskStruggleResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "AskOtherOpinions",
            "statement": "How do you think your family, friends or coworkers would react if they heard about you reaching your goal?",
            "response": self.AskOtherOpinionsResponse,
            "stateType": "AnswerResponse"
        },
        ]

    def AskStruggleStatement(self):
        #Load the data here because it is the first statement.
        self.shortTermData.readData()
        self.ID = self.shortTermData.data["id"]
        self.username = self.shortTermData.data["name"]
        self.goal = self.shortTermData.data["goal"]
        self.finalGoal = self.shortTermData["finalGoal"]
        self.milestone = self.shortTermData["milestone"]
        return "What are you struggling with?"

    def AskStruggleResponse(self, response):
        nextState = "AskOtherOpinions"
        #Save everything to the file
        self.struggle = response
        self.shortTermData.data["experiences"].append({
            "Question": "What are you struggling with?",
            "Answer": response,
            "session": 2
        })
        return [], nextState

    def AskOtherOpinionsResponse(self, response):
        nextState = "ContinueAfterStatusUpdateSession2"
        #Save everything to the file
        self.struggle = response
        self.shortTermData.data["experiences"].append({
            "Question": "How do you think your family, friends or coworkers would react if they heard about you reaching your goal?",
            "Answer": response,
            "session": 2
        })
        return [], nextState