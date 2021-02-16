import management_utils.response_manager as ResponseManager
import data_retrieval.memoryManager as shortTermData

class Session3Start:
    def __init__(self):
        self.responseUtils = ResponseManager.ResponseManager()
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
            "name": "Session3Start",
            "statement": self.Session3StartStatement,
            "response": "ReviewOfGoalsAndExpectationsSession3",
            "stateType": "Statement"
        },
        {
            "name": "ReviewOfGoalsAndExpectationsSession3",
            "statement": self.ReviewOfGoalsAndExpectationsStatement,
            "response": "DetermineProgressSession2",
            "stateType": "Statement"
        },
        {
            "name": "DetermineProgressSession3",
            "statement": self.DetermineProgressStatement,
            "response": self.DetermineProgressResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ConfirmProgressSession3",
            "statement": self.ConfirmProgressStatement,
            "response": self.ConfirmProgressResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "AchievementReachedSession3",
            "statement": "Congratulations, you have reached your goal",
            "response": "RetrospectiveSession3",
            "stateType": "Statement"
        },
        {
            "name": "AchievementNotReachedSession3",
            "statement": "Unfortunately, you have not reached your goal",
            "response": "RetrospectiveSession3",
            "stateType": "Statement"
        },
        {
            "name": "RetrospectiveSession3",
            "statement": "Let's talk about what went right and what went wrong",
            "response": "ReviewFirstSessionSession3",
            "stateType": "Statement"
        },
        {
            "name": "RetrospectiveSession3",
            "statement": "Let's talk about what went right and what went wrong",
            "response": "ReviewFirstSessionSession3",
            "stateType": "Statement"
        },
        {
            "name": "ReviewFirstSessionSession3",
            "statement": self.ReviewFirstSessionStatement,
            "response": self.ReviewFirstSessionStatementResponse,
            "stateType": "Statement"
        },
        {
            "name": "ReviewFirstSessionExperienceSuccessSession3",
            "statement": self.ReviewFirstSessionExperienceSuccessStatement,
            "response": "FirstMilestoneReached",
            "stateType": "Statement"
        },
        {
            "name": "ReviewFirstSessionExperienceFailureSession3",
            "statement": self.ReviewFirstSessionExperienceFailureStatement,
            "response": "FirstMilestoneNotReached",
            "stateType": "Statement"
        },
        {
            "name": "FirstMilestoneReached",
            "statement": self.ReviewFirstSessionExperienceSuccessStatement,
            "response": "FirstMilestoneReached",
            "stateType": "Statement"
        },
        {
            "name": "FirstMilestoneNotReached",
            "statement": self.ReviewFirstSessionExperienceFailureStatement,
            "response": "ReviewSecondSession",
            "stateType": "Statement"
        },
        ]

    def Session3StartStatement(self):
        #Load the data here because it is the first statement.
        self.shortTermData.readData()
        self.ID = self.shortTermData.data["id"]
        self.username = self.shortTermData.data["name"]
        self.goal = self.shortTermData.data["goal"]
        self.finalGoal = self.shortTermData.data["finalGoal"]
        self.milestone = self.shortTermData.data["milestone"]
        return "Welcome back " + self.username + ". How have you been? This is your third session. I hope you managed to meet your final goal."

    def ReviewOfGoalsAndExpectationsStatement(self):
        statement = "So, the diet related goal that you chose was "
        if self.goal is 0:
            statement = statement + "calorie restriction. Your goal is a caloric intake of " + str(self.finalGoal) + " calories."
            statement = statement + " When we last met, you managed to reach a caloric intake of " + str(self.shortTermData.data["diet"]["session2"]["calories"]) + " calories."
            statement = statement + " This means that to reach your final goal, you had " + str((self.shortTermData.data["diet"]["session2"]["calories"] - self.finalGoal)) + " calories left."
        else:
            statement = statement + "sugar reduction. Your goal is a sugar intake of " + str(self.finalGoal) + " grams of sugar."
            statement = statement + " When we last met, you managed to reach a sugar intake of " + str(self.shortTermData.data["diet"]["session2"]["sugar"]) + " grams of sugar."
            statement = statement + " This means that to reach your final goal, you had " + str((self.shortTermData.data["diet"]["session2"]["sugar"] - self.finalGoal)) + " grams of sugar left."
        return statement

    def DetermineProgressStatement(self):
        statement = "So did you meet your goal? "
        if self.goal is 0:
            statement = statement + "What was your daily caloric intake yesterday?"
        else:
            statement = statement + "What was your daily sugar intake yesterday?"
        return statement

    def DetermineProgressResponse(self, response):
        nextState = "ConfirmProgressSession3"
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
        nextState = "DetermineProgressSession3"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "DetermineProgressSession3"
        else:
            self.shortTermData.data["diet"]["session3"] = {}
            if self.goal is 0:
                self.shortTermData.data["diet"]["session3"]["calories"] = self.newCalories
                if self.newCalories > self.finalGoal:
                    nextState = "AchievementNotReachedSession3"
                    self.shortTermData.data["diet"]["session3"]["progressSufficient"] = False
                else:
                    nextState = "AchievementReachedSession3"
                    self.shortTermData.data["diet"]["session3"]["progressSufficient"] = True
            else:
                self.shortTermData.data["diet"]["session3"]["sugar"] = self.newSugar
                if self.newSugar > self.finalGoal:
                    nextState = "AchievementNotReachedSession3"
                    self.shortTermData.data["diet"]["session3"]["progressSufficient"] = False
                else:
                    nextState = "AchievementReachedSession3"
                    self.shortTermData.data["diet"]["session3"]["progressSufficient"] = True
        return [], nextState

    def ReviewFirstSessionStatement(self):
        return ""