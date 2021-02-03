import management_utils.response_manager as ResponseManager
import management_utils.search_based_conversation as SBC
import data_retrieval.memoryManager as shortTermData
import management_utils.diabetesConversation as diabetesConversation


class Session1Start:
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
            "response": "CurrentFeelings",
            "stateType": "Statement"
        },
        {
            "name": "CurrentFeelings",
            "statement": "Are you feeling excited to start? Nervous? What feelings are you having right now?",
            "response": self.CurrentFeelingsResponse,
            "stateType": "AnswerResponse"
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
            "statement": "There are two possible goals that you can choose. These are calorie restriction, and sugar reduction. Before we choose a goal, I would like to ask you for a few personal details so that we can ensure that the goal that is chosen is appropriate for you.",
            "response": "AskGender",
            "stateType": "Statement"
        },
        {
            "name": "AskGender",
            "statement": "What is your gender?",
            "response": self.AskGenderResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ConfirmGender",
            "statement": self.ConfirmGenderStatement,
            "response": self.ConfirmGenderResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "AskAge",
            "statement": "What is your age in years?",
            "response": self.AskAgeResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ConfirmAge",
            "statement": self.ConfirmAgeStatement,
            "response": self.ConfirmAgeResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "AskWeight",
            "statement": "What is your weight in kilograms?",
            "response": self.AskWeightResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ConfirmWeight",
            "statement": self.ConfirmWeightStatement,
            "response": self.ConfirmWeightResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "AskHeight",
            "statement": "What is your height in centimeters?",
            "response": self.AskHeightResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ConfirmHeight",
            "statement": self.ConfirmHeightStatement,
            "response": self.ConfirmHeightResponse,
            "stateType": "AnswerResponse"
        }
        ]

    def GetStartedGreetingStatement(self):
        #Load the data here because it is the first statement.
        self.shortTermData.readData()
        self.ID = self.shortTermData.data["id"]
        self.username = self.shortTermData.data["name"]
        self.shortTermData.data["physicalData"] = {}
        return "Great. Nice to meet you " + self.username + ". Let's start improving your diet"

    def AnswerDiabetesQuestionsResponse(self, response):
        nextState = "AskDiabetesQuestion"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "ListGoals"
        else:
            nextState = "AskDiabetesQuestion"
        return [], nextState

    def CurrentFeelingsResponse(self, response):
        nextState = "AnswerDiabetesQuestions"
        self.shortTermData.data["experiences"] = []
        self.shortTermData.data["experiences"].append({
            "Question": "Are you feeling excited to start? Nervous? What feelings are you having right now?",
            "Answer": response,
            "session": 1
        })

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

    def AskGenderResponse(self, response):
        nextState = "ConfirmGender"
        gender =  self.responseUtils.DetermineGender(response)
        if gender is 0:
            self.gender = "female"
        elif gender is 1:
            self.gender = "male"
        else:
            self.gender = "undefined"
        return [], nextState

    def ConfirmGenderStatement(self):
        return "Your gender is " + self.gender + ". Do I have that right?"

    def ConfirmGenderResponse(self, response):
        nextState = "AskGender"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "AskGender"
        else:
            self.shortTermData.data["physicalData"]["gender"] = self.gender
            nextState = "AskAge"
        return [], nextState

    def AskAgeResponse(self, response):
        nextState = "ConfirmAge"
        numbers = self.responseUtils.GetNumber(response)
        if len(numbers) > 0:
            self.age = numbers[0]
        return [], nextState

    def ConfirmAgeStatement(self):
        return "You are " + str(self.age) + " years old. Is this correct?"

    def ConfirmAgeResponse(self, response):
        nextState = "AskAge"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "AskAge"
        else:
            self.shortTermData.data["physicalData"]["age"] = self.age
            self.shortTermData.writeData()
            nextState = "AskWeight"
        return [], nextState

    def AskWeightResponse(self, response):
        nextState = "ConfirmWeight"
        numbers = self.responseUtils.GetNumber(response)
        if len(numbers) > 0:
            self.weight = numbers[0]
        return [], nextState

    def ConfirmWeightStatement(self):
        return "Your weight is " + str(self.weight) + " kilograms. Is that right?"

    def ConfirmWeightResponse(self, response):
        nextState = "AskWeight"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "AskWeight"
        else:
            self.shortTermData.data["physicalData"]["weight"] = self.weight
            nextState = "AskHeight"
        return [], nextState

    def AskHeightResponse(self, response):
        nextState = "ConfirmHeight"
        numbers = self.responseUtils.GetNumber(response)
        if len(numbers) > 0:
            self.height = numbers[0]
        return [], nextState

    def ConfirmHeightStatement(self):
        return "Your height is " + str(self.height) + " centimeters. Is that correct?"

    def ConfirmHeightResponse(self, response):
        nextState = "AskHeight"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "AskHeight"
        else:
            self.shortTermData.data["physicalData"]["height"] = self.height
            self.shortTermData.writeData()
            nextState = "ListGoals2"
        return [], nextState