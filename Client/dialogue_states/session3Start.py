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
            "response": "DetermineProgressSession3",
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
        }
        ]

    def Session3StartStatement(self):
        #Load the data here because it is the first statement.
        self.shortTermData.readData()
        self.ID = self.shortTermData.data["id"]
        self.username = self.shortTermData.data["name"]
        self.goal = self.shortTermData.data["goal"]
        self.finalGoal = self.shortTermData.data["finalGoal"]
        self.milestone = self.shortTermData.data["milestone"]

        if "condition" in self.shortTermData.data:
            self.condition = self.shortTermData.data["condition"]
        else:
            self.condition = 2
            self.shortTermData.data["condition"] = 2

        return "Welcome back " + self.username + ". How have you been? This is your third session. I hope you managed to meet your final goal."

    def ReviewOfGoalsAndExpectationsStatement(self):
        statement = "So, the diet related goal that you chose was "
        if self.goal is 0:
            statement = statement + "calorie restriction. Your goal is a caloric intake of " + str(self.finalGoal) + " calories."
            statement = statement + " When we last met, you managed to reach a caloric intake of " + str(self.shortTermData.data["diet"]["session2"]["calories"]) + " calories."
            achievementNumber = (self.shortTermData.data["diet"]["session2"]["calories"] - self.finalGoal)
            statement = statement + " This means that to reach your final goal, you had " + str(achievementNumber) + " calories left."
            if achievementNumber < 0:
                statement = statement + " Although you overshot your final goal, consistency is what makes a habit, so let's find out what changed since our previous session."
            elif achievementNumber == 0:
                statement = statement + " Although you met your final goal, consistency is what makes a habit, so let's find out what changed since our previous session."
        else:
            statement = statement + "sugar reduction. Your goal is a sugar intake of " + str(self.finalGoal) + " grams of sugar."
            statement = statement + " When we last met, you managed to reach a sugar intake of " + str(self.shortTermData.data["diet"]["session2"]["sugar"]) + " grams of sugar."
            achievementNumber = (self.shortTermData.data["diet"]["session2"]["sugar"] - self.finalGoal)
            statement = statement + " This means that to reach your final goal, you had " + str(achievementNumber) + " grams of sugar left."
            if achievementNumber < 0:
                statement = statement + " Although you overshot your final goal, consistency is what makes a habit, so let's find out what changed since our previous session."
            elif achievementNumber == 0:
                statement = statement + " Although you met your final goal, consistency is what makes a habit, so let's find out what changed since our previous session."
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
        else:
            #In the case that there are no numbers, just use a default until it is fixed
            if self.goal is 0:
                self.newCalories = self.finalGoal
            else:
                self.newSugar = self.finalGoal
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
            self.shortTermData.writeData()
        return [], nextState