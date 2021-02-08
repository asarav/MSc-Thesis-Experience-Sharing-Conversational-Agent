import management_utils.response_manager as ResponseManager
import management_utils.search_based_conversation as SBC
import data_retrieval.memoryManager as shortTermData
import management_utils.diabetesConversation as diabetesConversation
import diet_utils.mileStone as milestone


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
        },
        {
            "name": "LessAmbitiousGoal",
            "statement": "Since you have not met your milestone, would you like to work towards a less ambitious goal for your final goal?",
            "response": self.LessAmbitiousGoalResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "MoreAmbitiousGoal",
            "statement": "Since you have greatly exceeded your milestone, would you like to work towards a more ambitious goal for your final goal?",
            "response": self.MoreAmbitiousGoalResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "PresentAndConfirmEasierGoal",
            "statement": self.PresentAndConfirmEasierGoalStatement,
            "response": self.PresentAndConfirmEasierGoalResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "PresentAndConfirmHarderGoal",
            "statement": self.PresentAndConfirmHarderGoalStatement,
            "response": self.PresentAndConfirmHarderGoalStatement,
            "stateType": "AnswerResponse"
        },
        {
            "name": "NewGoalChosen",
            "statement": "Then we will continue with this new goal in mind.",
            "response": "AskFeelingsAboutProgress",
            "stateType": "Statement"
        },
        {
            "name": "AskFeelingsSession2",
            "statement": "Now that you have started, how do you feel about the progress you have made?",
            "response": self.AskFeelingsResponse,
            "stateType": "AnswerResponse"
        },
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
                self.shortTermData.data["session2Progress"]["sugar"] = self.newCalories
                if self.newSugar > self.milestone:
                    nextState = "ProgressInsufficientSession2"
                else:
                    nextState = "ProgressSufficientSession2"
            nextState = ""
        return [], nextState

    def ProgressSufficientStatement(self):
        statement = "Looks like you are on track to reach "
        if self.goal is 0:
            statement = statement + self.goal + " calories in your daily caloric intake."
        else:
            statement = statement + self.goal + " grams of sugar in your daily sugar intake."
        return statement + " Great job!"

    def ProgressInsufficientStatement(self):
        statement = "It looks like you are falling behind. At the current rate, you will not reach your final goal of "
        if self.goal is 0:
            statement = statement + self.goal + " maximum calories in your daily caloric intake."
        else:
            statement = statement + self.goal + " maximum grams of sugar in your daily sugar intake."
        return statement

    def SharedMemoryReferencePraise(self):
        return self.shortTermData.chooseMemory(session=1, type=0)

    def SharedMemoryReferenceCriticsm(self):
        return self.shortTermData.chooseMemory(session=1, type=0)

    def IncreaseDifficultyOrContinue(self, response):
        nextState = "AskFeelingsSession2"
        if self.goal is 0:
            if self.newCalories > self.finalGoal or self.newCalories > (self.milestone + (self.finalGoal - self.milestone)/2):
                nextState = "MoreAmbitiousGoal"
        else:
            if self.newSugar > self.finalGoal or self.newSugar > (self.milestone + (self.finalGoal - self.milestone)/2):
                nextState = "MoreAmbitiousGoal"
        return [], nextState

    def LessAmbitiousGoalResponse(self, response):
        nextState = "PresentAndConfirmEasierGoal"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "AskFeelingsAboutProgress"
        else:
            nextState = "PresentAndConfirmEasierGoal"
        return [], nextState

    def MoreAmbitiousGoalResponse(self, response):
        nextState = "PresentAndConfirmHarderGoal"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "AskFeelingsAboutProgress"
        else:
            nextState = "PresentAndConfirmHarderGoal"
        return [], nextState

    def PresentAndConfirmEasierGoalStatement(self):
        if self.goal is 0:
            statement = "I propose that you change your final goal to be " + str(self.milestone) + " calories."
            return statement + " If you decide not to work toward this new goal, you can continue towards the originally planned goal. Would you like to work towards this easier goal?"
        else:
            statement = "I propose that you change your final goal to be " + str(self.milestone) + " grams of sugar."
            return statement + " If you decide not to work toward this new goal, you can continue towards the originally planned goal. Would you like to work towards this easier goal?"

    def PresentAndConfirmHarderGoalStatement(self):
        physicalData = self.shortTermData.data["physicalData"]
        age = physicalData["age"]
        weight = physicalData["weight"]
        height = physicalData["height"]
        gender = physicalData["gender"]
        getGoal = milestone.MileStone(age, weight, height, gender)
        if self.goal is 0:
            initialConsumption = self.shortTermData.data["diet"]["session1"]["calories"]
            self.newGoal = getGoal.generatedAmbitiousGoal(self.goal, initialConsumption)
            statement = "I propose that you change your final goal to be " + str(self.newCalories) + " calories."
            if self.newGoal == self.goal:
                statement = statement + " If the new goal is same as your previous goal, this is because your previous goal was on the boundary of what may have been considered safe."
            return statement + " If you decide not to work toward this new goal, you can continue towards the originally planned goal. Would you like to work towards this easier goal?"
        else:
            initialConsumption = self.shortTermData.data["diet"]["session1"]["sugar"]
            self.newGoal = getGoal.generatedAmbitiousGoal(self.goal, initialConsumption)
            statement = "I propose that you change your final goal to be " + str(self.milestone) + " grams of sugar."
            if self.newGoal == self.goal:
                statement = statement + " If the new goal is same as your previous goal, this is because your previous goal was on the boundary of what may have been considered safe."
            return statement + " If you decide not to work toward this new goal, you can continue towards the originally planned goal. Would you like to work towards this easier goal?"

    def PresentAndConfirmEasierGoalResponse(self, response):
        nextState = "AskFeelingsAboutProgress"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 1:
            self.shortTermData.data["previousGoal"] = self.finalGoal
            self.shortTermData.data["finalGoal"] = self.newGoal
            self.shortTermData.data["goalChanged"] = True
            self.finalGoal = self.newGoal
            nextState = "NewGoalChosen"
        return [], nextState

    def PresentAndConfirmHarderGoalStatement(self, response):
        nextState = "AskFeelingsAboutProgress"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 1:
            self.shortTermData.data["previousGoal"] = self.finalGoal
            self.shortTermData.data["finalGoal"] = self.newGoal
            self.shortTermData.data["goalChanged"] = True
            self.finalGoal = self.newGoal
            nextState = "NewGoalChosen"
        return [], nextState

    def AskFeelingsResponse(self, response):
        nextState = ""
        #Save everything to the file

        return [], nextState