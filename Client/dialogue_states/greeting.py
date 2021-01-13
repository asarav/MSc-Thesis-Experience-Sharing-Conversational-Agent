import management_utils.response_manager as ResponseManager
import data_retrieval.shortTermData as shortTermData

class Greeting:
    def __init__(self):
        self.responseUtils = ResponseManager.ResponseManager()
        self.ID = "1234"
        self.username = ""
        self.IncorrectName = False

        #Load the data here because it is the beginning of the interaction
        self.shortTermData = shortTermData.ShortTermData()
        self.shortTermData.readData()

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
            "statement": "What is your first name?",
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
        self.shortTermData.data["id"] = self.ID
        return "Okay. Welcome. Here is your new user Id. " + "Your ID is: " + self.ID + ". Make sure you write it down somewhere. You will need it for all of the sessions we will have together. Do you have your ID memorized and written down somewhere?"

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
            self.shortTermData.data["name"] = self.username
            self.shortTermData.writeData()
            nextState = "GetStartedGreeting"
        return [], nextState

    def IncorrectNameResponse(self, response):
        nextState = "ConfirmName"
        self.IncorrectName = True
        self.username = response
        return [], nextState