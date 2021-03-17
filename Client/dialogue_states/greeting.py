import management_utils.response_manager as ResponseManager
import data_retrieval.memoryManager as shortTermData
from data_retrieval.jsonManager import jsonManager


class Greeting:
    def __init__(self):
        self.responseUtils = ResponseManager.ResponseManager()
        self.ID = "1234"
        self.username = ""
        self.IncorrectName = False
        self.userIdFirstTime = True

        #Load the data here because it is the beginning of the interaction
        self.shortTermData = shortTermData.MemoryManager()
        self.shortTermData.readData()
        self.shortTermData.data = {}

        self.states = [{
            "name": "AskUserID",
            "statement": self.AskUserIDStatement,
            "response": self.AskUserIDResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ConfirmUserID",
            "statement": self.ConfirmUserIDStatement,
            "response": self.ConfirmUserIDResponse,
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
            "statement": "What is your first name, or what would you like to be called?",
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

    def AskUserIDStatement(self):
        if self.userIdFirstTime:
            self.userIdFirstTime = False
            return "Hello, I am Diet Bot. Before we start, what is your user id? Your user id is provided to you by Prolific."
        else:
            return "What is your user id?"

    def AskUserIDResponse(self, response):
        #Process the response here.
        nextState = "ConfirmUserID"
        self.ID = self.responseUtils.GetProlificId(response)

        return [], nextState

    def ConfirmUserIDStatement(self):
        return "Your user id is " + self.ID + ". Do I have that right?"

    def ConfirmUserIDResponse(self, response):
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "AskUserID"
        else:
            self.shortTermData.data["id"] = self.ID
            reader = jsonManager()
            fileExists = reader.readJSON("interaction_data/" + self.ID + ".json")
            if fileExists:
                #Load long term memory into short term memory
                self.shortTermData.readDataFromLongTermMemory(self.ID)
                session = self.shortTermData.data["session"]
                self.shortTermData.writeData()
                if session is 2:
                    nextState = "Session2Start"
                else:
                    nextState = "Session3Start"
            else:
                nextState = "Start"
        return [], nextState

    def AskNameResponse(self, response):
        nextState = "ConfirmName"
        print(response)
        self.username = self.responseUtils.GetName(response)
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