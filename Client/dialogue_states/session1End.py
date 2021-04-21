import management_utils.response_manager as ResponseManager
import management_utils.search_based_conversation as SBC
import data_retrieval.memoryManager as shortTermData
from management_utils import calorieRestrictionConversation
from management_utils import sugarRestrictionConversation
from management_utils.questionDetector import QuestionDetector


class Session1End:
    def __init__(self):
        self.responseUtils = ResponseManager.ResponseManager()
        self.calorieRestrictionAnswers = SBC.SearchBasedConversation(calorieRestrictionConversation.conversation, "Calorie Restriction Questions")
        self.sugarReductionAnswers = SBC.SearchBasedConversation(sugarRestrictionConversation.conversation, "Sugar Reduction Questions")
        self.questionDetector = QuestionDetector()
        self.username = ""
        self.gender = 0
        self.age = 18
        self.weight = 60
        self.height = 160
        self.askedGoals = False
        self.goal = 0
        self.caloriesConsumed = 2000
        self.sugarConsumed = 50
        self.askedConsumption = False
        self.firstTimeGoalsQuestion = True

        #Load user data
        self.shortTermData = shortTermData.MemoryManager()
        self.dataLoaded = False

        self.states = [
        {
            "name": "AskMilestoneQuestions",
            "statement": "Do you have any questions on how to reach this milestone?",
            "response": self.AskMilestoneQuestionsResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "AnswerGoalQuestions",
            "statement": self.AnswerGoalQuestionsStatement,
            "response": self.AnswerGoalQuestionsResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "AskGoalQuestion",
            "statement": "What is your question?",
            "response": self.AskGoalQuestionResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "GoalAnswer",
            "statement": self.ProvideGoalAnswer,
            "response": "AnswerGoalQuestions",
            "stateType": "Statement"
        },
        {
            "name": "AskFavoriteFood",
            "statement": "Do you have any foods you like in particular? What is your favorite food?",
            "response": self.AskFavoriteFoodResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "FavoriteFoodStatement",
            "statement": "A good way to start is to take your favorite food and find a healthier option to eat instead.",
            "response": "ReviewNextMilestone",
            "stateType": "Statement"
        },
        {
            "name": "ReviewNextMilestone",
            "statement": self.ReviewNextMilestoneStatement,
            "response": self.ReviewNextMilestoneResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "FurtherExplanation",
            "statement": self.FurtherExplanationStatement,
            "response": "Goodbye",
            "stateType": "Statement"
        },
        {
            "name": "Goodbye",
            "statement": "I will see you in the next session. Work hard and good luck on your diet. Bye.",
            "response": "",
            "stateType": "End"
        }
        ]

    def AskMilestoneQuestionsResponse(self, response):
        #Load the data here because it is the first statement.
        if self.dataLoaded is False:
            self.shortTermData.readData()
            #Load all the physical data into the class members
            physicalData = self.shortTermData.data["physicalData"]
            self.gender = physicalData["gender"]
            self.age = physicalData["age"]
            self.weight = physicalData["weight"]
            self.height = physicalData["height"]
            self.username = self.shortTermData.data["name"]
            self.ID = self.shortTermData.data["id"]
            self.goal = self.shortTermData.data["goal"]
            self.milestone = self.shortTermData.data["milestone"]
            self.finalGoal = self.shortTermData.data["finalGoal"]

            self.dataLoaded = True

        nextState = ""
        decision = self.responseUtils.YesOrNoSearch(response)
        if decision is 0:
            nextState = "AskFavoriteFood"
        else:
            nextState = "AskGoalQuestion"

        return [], nextState

    def AnswerGoalQuestionsResponse(self, response):
        nextState = "AskGoalQuestion"
        #Determine if a question is asked here. If not, go through the yes/no process
        if self.questionDetector.IsQuestion(response):
            self.GoalQuestionAnswer = ""
            if self.goal is 0:
                self.GoalQuestionAnswer = self.calorieRestrictionAnswers.askQuestion(response)
            else:
                self.GoalQuestionAnswer = self.sugarReductionAnswers.askQuestion(response)
            nextState = "GoalAnswer"
        else:
            decision = self.responseUtils.YesOrNoSearch(response)
            if decision is 0:
                nextState = "AskFavoriteFood"
            else:
                nextState = "AskGoalQuestion"
        return [], nextState

    def AskFavoriteFoodResponse(self, response):
        nextState = "FavoriteFoodStatement"
        #Try to extract just the relevant food
        stopwords = ["I", "i", "like", "my", "favorite", "is", "think", "food", "meal"]
        querywords = response.split()
        resultwords = [word for word in querywords if word.lower() not in stopwords]
        result = ' '.join(resultwords)

        self.shortTermData.data["dietLikes"] = {
            "question": result
        }
        self.shortTermData.writeData()
        return [], nextState

    def AnswerGoalQuestionsStatement(self):
        return "Do you have any other questions?"

    def AskGoalQuestionResponse(self, response):
        nextState = "GoalAnswer"
        self.GoalQuestionAnswer = ""
        if self.goal is 0:
            self.GoalQuestionAnswer = self.calorieRestrictionAnswers.askQuestion(response)
        else:
            self.GoalQuestionAnswer = self.sugarReductionAnswers.askQuestion(response)
        return [], nextState

    def ProvideGoalAnswer(self):
        return self.GoalQuestionAnswer

    def ReviewNextMilestoneStatement(self):
        statement = "Keep at it and you will get there. Before we end this session, let's review your next milestone to reach. Your next milestone is "
        if self.goal is 0:
            statement = statement + "to work your way down to a daily caloric consumption of " + str(self.milestone) + " calories."
        else:
            statement = statement + "to work your way down to a daily sugar consumption of " + str(self.milestone) + " grams of sugar."
        return statement + " This will get you halfway towards your final goal. Does that make sense?"

    def ReviewNextMilestoneResponse(self, response):
        nextState = ""
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "FurtherExplanation"
        else:
            nextState = "Goodbye"
        self.shortTermData.data["session"] = 2
        self.shortTermData.writeData()
        self.shortTermData.writeDataToLongTermMemory(self.shortTermData.data["id"])
        return [], nextState

    def FurtherExplanationStatement(self):
        statement = "Your milestone is "
        if self.goal is 0:
            statement = statement + str(self.milestone) + " maximum calories consumed in a day and the final goal is " + str(self.finalGoal) + " maximum calories consumed in a day."
            statement = statement + " This means that you should work on portion control, switching to healthy food items and generally watching what you eat."
        else:
            statement = statement + str(self.milestone) + " maximum grams of sugar consumed in a day and the final goal is " + str(self.finalGoal) + " maximum sugar consumed in a day."
            statement = statement + " This means that you should avoid added sugars, switching to healthy food items with reduced sugar and generally watching what you eat."
        return statement