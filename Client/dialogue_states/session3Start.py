import management_utils.response_manager as ResponseManager
import management_utils.search_based_conversation as SBC
import data_retrieval.memoryManager as shortTermData
import management_utils.diabetesConversation as diabetesConversation
import diet_utils.mileStone as milestone


class Session3Start:
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
        self.shortTermData.data["session"] = 3

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
        },
        {
            "name": "ProgressSufficientSession2",
            "statement": self.ProgressSufficientStatement,
            "response": "SharedMemoryReferencePraiseSession2",
            "stateType": "Statement"
        },
        {
            "name": "ProgressInsufficientSession2",
            "statement": self.ProgressInsufficientStatement,
            "response": "SharedMemoryReferenceCriticismSession2",
            "stateType": "Statement"
        },
        {
            "name": "SharedMemoryReferencePraiseSession2",
            "statement": self.SharedMemoryReferencePraise,
            "response": self.IncreaseDifficultyOrContinue,
            "stateType": "Statement"
        },
        {
            "name": "SharedMemoryReferenceCriticismSession2",
            "statement": self.SharedMemoryReferenceCriticsm,
            "response": "LessAmbitiousGoal",
            "stateType": "Statement"
        }
        ]

    def Session2StartStatement(self):
        #Load the data here because it is the first statement.
        self.shortTermData.readData()
        self.ID = self.shortTermData.data["id"]
        self.username = self.shortTermData.data["name"]
        self.goal = self.shortTermData.data["goal"]
        self.finalGoal = self.shortTermData.data["finalGoal"]
        self.milestone = self.shortTermData.data["milestone"]
        return "Welcome back " + self.username + ". How have you been? This is your third session. I hope you managed to meet your milestone."

    def ReviewOfGoalsAndExpectationsStatement(self):
        statement = "So, the diet related goal that you chose was "
        if self.goal is 0:
            statement
        else:
            statement
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
        statement = ""
        if self.goal is 0:
            statement = statement + "Your caloric intake was " + str(self.newCalories) + " calories. Is this correct?"
        else:
            statement = statement + "Your sugar intake was " + str(self.newSugar) + " grams of sugar. Is this correct?"
        return statement

    def ConfirmProgressResponse(self, response):
        nextState = "DetermineProgressSession2"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "DetermineProgressSession2"
        else:
            self.shortTermData.data["session2Progress"] = {}
            if self.goal is 0:
                self.shortTermData.data["session2Progress"]["calories"] = self.newCalories
                if self.newCalories > self.milestone:
                    nextState = "ProgressInsufficientSession2"
                else:
                    nextState = "ProgressSufficientSession2"
            else:
                self.shortTermData.data["session2Progress"]["sugar"] = self.newSugar
                if self.newSugar > self.milestone:
                    nextState = "ProgressInsufficientSession2"
                else:
                    nextState = "ProgressSufficientSession2"
        return [], nextState

    def ProgressSufficientStatement(self):
        statement = "Looks like you are on track to reach "
        if self.goal is 0:
            statement = statement + str(self.finalGoal) + " calories in your daily caloric intake."
        else:
            statement = statement + str(self.finalGoal) + " grams of sugar in your daily sugar intake."
        return statement + " Great job!"

    def ProgressInsufficientStatement(self):
        statement = "It looks like you are falling behind. At the current rate, you will not reach your final goal of "
        if self.goal is 0:
            statement = statement + str(self.finalGoal) + " maximum calories in your daily caloric intake."
        else:
            statement = statement + str(self.finalGoal) + " maximum grams of sugar in your daily sugar intake."
        return statement

    def SharedMemoryReferencePraise(self):
        return self.shortTermData.chooseMemory(session=1, type=0)

    def SharedMemoryReferenceCriticsm(self):
        return self.shortTermData.chooseMemory(session=1, type=1)