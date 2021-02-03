import management_utils.response_manager as ResponseManager
import management_utils.search_based_conversation as SBC
import data_retrieval.memoryManager as shortTermData
import management_utils.diabetesConversation as diabetesConversation


class Session2Start:
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
            "name": "Session2Start",
            "statement": self.Session2StartStatement,
            "response": "ReviewOfGoalsAndExpectationsSession2",
            "stateType": "Statement"
        },
        {
            "name": "ReviewOfGoalsAndExpectationsSession2",
            "statement": self.ReviewOfGoalsAndExpectationsStatement,
            "response": "DetermineProgressSession2",
            "stateType": "Statement"
        },
        {
            "name": "DetermineProgressSession2",
            "statement": self.DetermineProgressStatement,
            "response": self.DetermineProgressResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ConfirmProgressSession2",
            "statement": self.ConfirmProgressStatement,
            "response": self.ConfirmProgressResponse,
            "stateType": "AnswerResponse"
        }
        ]

    def Session2StartStatement(self):
        #Load the data here because it is the first statement.
        self.shortTermData.readData()
        self.ID = self.shortTermData.data["id"]
        self.username = self.shortTermData.data["name"]
        self.goal = self.shortTermData.data["goal"]
        self.finalGoal = self.shortTermData["finalGoal"]
        self.milestone = self.shortTermData["milestone"]
        return "Welcome back " + self.username + ". How have you been? This is your second session. I hope you managed to meet your milestone."

    def ReviewOfGoalsAndExpectationsStatement(self):
        statement = "So, the diet related goal that you chose was "
        if self.goal is 0:
            statement = statement + "calorie restriction. When we last met, you were given a final goal of " + str(self.finalGoal) + " maximum calories consumed in a day."
            statement = statement + " To reach this, you were given a milestone of a daily caloric intake of " + str(self.milestone) + " calories to reach by today."
        else:
            statement = statement + "sugar reduction. When we last met, you were given a final goal of " + str(self.finalGoal) + " maximum grams of sugar consumed in a day."
            statement = statement + " To reach this, you were given a milestone of a daily sugar intake of " + str(self.milestone) + " grams of sugar to reach by today."
        return statement

    def DetermineProgressStatement(self):
        statement = "So did you meet your goal? "
        if self.goal is 0:
            statement = statement + "What was your daily caloric intake yesterday?"
        else:
            statement = statement + "What was your daily sugar intake yesterday?"
        return statement

    def DetermineProgressResponse(self, response):
        nextState = "ConfirmProgressSession2"
        numbers = self.responseUtils.GetNumber(response)
        if len(numbers) > 0:
            if self.goal is 0:
                self.newCalories = numbers[0]
            else:
                self.newSugar = numbers[0]
        return [], nextState

    def ConfirmProgressStatement(self):
        return

    def ConfirmProgressResponse(self, response):
        nextState = ""
        return [], nextState