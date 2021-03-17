import management_utils.response_manager as ResponseManager
import data_retrieval.memoryManager as shortTermData

class Session3Retrospective:
    def __init__(self):
        self.responseUtils = ResponseManager.ResponseManager()
        self.ID = "1234"
        self.username = ""
        self.firstTimeDiabetesQuestion = True
        self.gender = 0
        self.age = 18
        self.weight = 60
        self.height = 160
        self.dataLoaded = False

        #Load user data
        self.shortTermData = shortTermData.MemoryManager()
        self.shortTermData.data["session"] = 3

        self.goalChangedAmbitious = False
        self.goalChangedEasier = False

        self.states = [
        {
            "name": "ReviewFirstSessionSession3",
            "statement": self.ReviewFirstSessionStatement,
            "response": self.ReviewFirstSessionStatementResponse,
            "stateType": "Statement"
        },
        {
            "name": "FirstMilestoneReachedSession3",
            "statement": self.ReviewFirstSessionExperienceSuccessStatement,
            "response": self.FirstMilestoneExperienceReflectionSelect,
            "stateType": "Statement"
        },
        {
            "name": "FirstMilestoneNotReachedSession3",
            "statement": self.ReviewFirstSessionExperienceFailureStatement,
            "response": self.FirstMilestoneExperienceReflectionSelect,
            "stateType": "Statement"
        },
        {
            "name": "FirstMilestoneExperienceReflectionSession3",
            "statement": self.FirstMilestoneExperienceReflection,
            "response": "AskFirstExperienceOpinionSession3",
            "stateType": "Statement"
        },
        {
            "name": "AskFirstExperienceOpinionSession3",
            "statement": self.AskFirstExperienceOpinionStatement,
            "response": self.AskFirstExperienceOpinionResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ReviewSecondSessionSession3",
            "statement": self.ReviewSecondSessionStatement,
            "response": self.ReviewSecondSessionStatementResponse,
            "stateType": "Statement"
        },
        {
            "name": "FinalGoalReachedSession3",
            "statement": self.ReviewSecondSessionExperienceSuccessStatement,
            "response": self.FinalGoalExperienceReflectionSelect,
            "stateType": "Statement"
        },
        {
            "name": "FinalGoalNotReachedSession3",
            "statement": self.ReviewSecondSessionExperienceFailureStatement,
            "response": self.FinalGoalExperienceReflectionSelect,
            "stateType": "Statement"
        },
        {
            "name": "FinalGoalExperienceReflectionSession3",
            "statement": self.FinalGoalExperienceReflection,
            "response": "AskFinalGoalExperienceOpinion",
            "stateType": "Statement"
        },
        {
            "name": "AskFinalGoalExperienceOpinion",
            "statement": self.AskFinalGoalExperienceOpinionStatement,
            "response": self.AskFinalGoalExperienceOpinionResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "OverallProgressStatement",
            "statement": self.OverallProgressStatement,
            "response": "FutureWorkSession3",
            "stateType": "Statement"
        },
        {
            "name": "FutureWorkSession3",
            "statement": self.FutureWorkSession3,
            "response": "AskOpinionFutureWorkSession3",
            "stateType": "Statement"
        },
        {
            "name": "AskOpinionFutureWorkSession3",
            "statement": "So, what do you think? Do you think you will continue to work on your diet by yourself?",
            "response": self.AskOpinionFutureWorkResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "FutureWorkWarningSession3",
            "statement": "If you do decide to continue working on your diet, just remember to keep your goals manageable and safe. If you are in doubt as to whether your goals pose a health risk, please consult with your doctor or the appropriate health professional.",
            "response": "ValedictionSession3",
            "stateType": "Statement"
        },
        {
            "name": "ValedictionSession3",
            "statement": self.ValedictionSessionStatement,
            "response": "",
            "stateType": "End"
        }
        ]

    def ReviewFirstSessionStatement(self):
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

        statement = "In our first session, you were given a milestone of " + str(self.milestone)
        if self.goal is 0:
            statement = statement + " calories to reach."
        else:
            statement = statement + " grams of sugar to reach."
        return statement

    def ReviewFirstSessionStatementResponse(self, response):
        nextState = ""
        if self.goal is 0:
            #Check if caloric intake is less than or equal to milestone
            caloricIntake = self.shortTermData.data["diet"]["session2"]["calories"]
            if caloricIntake <= self.milestone:
                nextState = "FirstMilestoneReachedSession3"
            else:
                nextState = "FirstMilestoneNotReachedSession3"
        else:
            #Check if sugar intake is less than or equal to milestone :
            sugarIntake = self.shortTermData.data["diet"]["session2"]["sugar"]
            if sugarIntake <= self.milestone:
                nextState = "FirstMilestoneReachedSession3"
            else:
                nextState = "FirstMilestoneNotReachedSession3"

        return [], nextState

    def ReviewFirstSessionExperienceSuccessStatement(self):
        self.milestoneSuccess = True
        statement = "By our second session, you have managed to reach this milestone and took your first step towards your goal."
        if "goalChanged" in self.shortTermData.data:
            goalChanged = self.shortTermData.data["goalChanged"]
            if goalChanged:
                self.goalChangedAmbitious = True
                self.goalChangedEasier = False
                statement = statement + " And because you did so well, you were given the option of working towards a more ambitious goal which you took."
        return statement

    def ReviewFirstSessionExperienceFailureStatement(self):
        self.milestoneSuccess = False
        statement = "Unfortunately, you were unable to reach this milestone by our second session which put you at a disadvantage."
        if "goalChanged" in self.shortTermData.data:
            goalChanged = self.shortTermData.data["goalChanged"]
            if goalChanged:
                self.goalChangedAmbitious = False
                self.goalChangedEasier = True
                statement = statement + " Because you struggled, you were given the option of working towards a less ambitious goal which you took."
        return statement

    def FirstMilestoneExperienceReflectionSelect(self, response):
        nextState = ""
        if self.condition is 0:
            nextState = "ReviewSecondSessionSession3"
        else:
            nextState = "FirstMilestoneExperienceReflectionSession3"
        return [], nextState

    def FirstMilestoneExperienceReflection(self):
        if self.milestoneSuccess:
            return self.shortTermData.chooseMemory(session=1, type=0, condition=self.condition)
        else:
            return self.shortTermData.chooseMemory(session=1, type=1, condition=self.condition)

    def AskFirstExperienceOpinionStatement(self):
        return "Do you agree or disagree with this statement regarding your milestone? Why or why not?"

    def AskFirstExperienceOpinionResponse(self, response):
        #For now, we won't do anything with the response
        #Store the response, whether they agree or disagree

        return [], "ReviewSecondSessionSession3"

    def ReviewSecondSessionStatement(self):
        statement = "In our second session, you were told to reach your final goal of " + str(self.finalGoal)
        if self.goal is 0:
            statement = statement + " calories to reach before we met today."
        else:
            statement = statement + " grams of sugar to reach before we met today."
        return statement

    def ReviewSecondSessionStatementResponse(self, response):
        nextState = ""
        if self.goal is 0:
            #Check if caloric intake is less than or equal to milestone
            caloricIntake = self.shortTermData.data["diet"]["session3"]["calories"]
            if caloricIntake <= self.finalGoal:
                nextState = "FinalGoalReachedSession3"
            else:
                nextState = "FinalGoalNotReachedSession3"
        else:
            #Check if sugar intake is less than or equal to milestone :
            sugarIntake = self.shortTermData.data["diet"]["session3"]["sugar"]
            if sugarIntake <= self.finalGoal:
                nextState = "FinalGoalReachedSession3"
            else:
                nextState = "FinalGoalNotReachedSession3"

        return [], nextState

    def ReviewSecondSessionExperienceSuccessStatement(self):
        self.finalGoalSuccess = True
        return "Today you reached your final goal and ultimately achieved an improvement in your diet habits."

    def ReviewSecondSessionExperienceFailureStatement(self):
        self.finalGoalSuccess = False
        return "Unfortunately, you did not reach your final goal, which means that there is more work that must be done to successfully gain an improvement in your diet habits."

    def FinalGoalExperienceReflectionSelect(self, response):
        nextState = ""
        if self.condition is 0 or self.condition is 1:
            nextState = "OverallProgressStatement"
        else:
            nextState = "FinalGoalExperienceReflectionSession3"
        return [], nextState

    def FinalGoalExperienceReflection(self):
        if self.finalGoalSuccess:
            return self.shortTermData.chooseMemory(session=2, type=0, condition=self.condition)
        else:
            return self.shortTermData.chooseMemory(session=2, type=1, condition=self.condition)

    def AskFinalGoalExperienceOpinionStatement(self):
        return "So, what do you think? Do you feel the same way or do you have a different opinion?"

    def AskFinalGoalExperienceOpinionResponse(self, response):
        self.shortTermData.data["ExperienceResponse"].append({
            "answer": response,
            "agree": self.responseUtils.YesOrNo(response)
        })
        return [], "OverallProgressStatement"

    def OverallProgressStatement(self):
        if self.milestoneSuccess and self.finalGoalSuccess:
            return "Overall, it looks like everything went well for you and you knocked everything out of the park"
        elif not self.milestoneSuccess and self.finalGoalSuccess:
            return "Overall, It looks like you struggled a bit in the beginning with your milestone, but you came through in the end and managed to reach your goal."
        elif self.milestoneSuccess and not self.finalGoalSuccess:
            return "Overall, although you did not meet your final goal, you did at least make some progress and meet your milestone which means that you were able to take the first step and showed initiative in working towards bettering your health."
        else:
            return "Overall, it looks like you did not meet your milestone or your final goal which suggests that you struggle to take the first step and perhaps maybe if that is where you struggle, smaller steps may be necessary."

    def FutureWorkSession3(self):
        if self.finalGoalSuccess:
            return "Now that you have met your final goal, you can try to maintain your current diet, or work towards more ambitious goals on your own. You can work at your own pace. Aim for what is best for you."
        else:
            return "Since you have not reached your final goal, what you can do in the future is try to break up goals into even more manageable chunks and work on them over a longer period of time to reduce the difficulty. Since consistency is what matters, as long as you are doing something everyday, you are making progress and will eventually reach your goal."

    def AskOpinionFutureWorkResponse(self, response):
        self.shortTermData.data["FutureWork"] = []
        self.shortTermData.data["FutureWork"].append({
            "answer": response,
            "agree": self.responseUtils.YesOrNo(response)
        })
        return [], "FutureWorkWarningSession3"

    def ValedictionSessionStatement(self):
        name = self.shortTermData.data["name"]
        #Save data
        self.shortTermData.data["session"] = 4
        self.shortTermData.writeData()
        self.shortTermData.writeDataToLongTermMemory(self.shortTermData.data["id"])
        return "Thank you for spending these sessions with me " + str(name) + " to work on your diet. If you stay focused, determined, and consistent you will eventually get wherever it is you want to be. I hope you enjoy the rest of your day and the rest of your journey towards managing your diet. Goodbye."