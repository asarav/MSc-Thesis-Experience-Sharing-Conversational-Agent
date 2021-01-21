import management_utils.response_manager as ResponseManager
import management_utils.search_based_conversation as SBC
import data_retrieval.shortTermData as shortTermData
from diet_utils.nutrition import Nutrition


class Session1GoalSetting:
    def __init__(self):
        self.responseUtils = ResponseManager.ResponseManager()
        #I might be able to remove this line
        self.DiabetesAnswers = SBC.SearchBasedConversation([], "Diabetes Questions")
        self.username = ""
        self.gender = 0
        self.age = 18
        self.weight = 60
        self.height = 160
        self.askedGoals = False
        self.goal = 0
        self.caloriesConsumed = 2000
        self.sugarConsumed = 50

        #Load user data
        self.shortTermData = shortTermData.ShortTermData()

        self.states = [
        {
            "name": "ListGoals2",
            "statement": self.ListGoals2Statement,
            "response": "ExplainGoals",
            "stateType": "Statement"
        },
        {
            "name": "ExplainGoals",
            "statement": self.ExplainGoalsStatement,
            "response": "ExplainGoals",
            "stateType": "Statement"
        },
        {
            "name": "AskGoals",
            "statement": self.AskGoalsStatement,
            "response": self.AskGoalsResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ConfirmGoal",
            "statement": self.ConfirmGoalStatement,
            "response": self.ConfirmGoalResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "AskCurrentConsumption",
            "statement": self.AskCurrentConsumptionStatement,
            "response": self.AskCurrentConsumptionResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ConfirmCurrentConsumption",
            "statement": self.ConfirmCurrentConsumptionStatement,
            "response": self.ConfirmCurrentConsumptionResponse,
            "stateType": "AnswerResponse"
        }
        ]

    def ListGoals2Statement(self):
        #Load the data here because it is the first statement.
        self.shortTermData.readData()
        #Load all the physical data into the class members
        physicalData = self.shortTermData.data["physicalData"]
        self.gender = physicalData["gender"]
        self.age = physicalData["age"]
        self.weight = physicalData["age"]
        self.height = physicalData["age"]
        self.username = self.shortTermData.data["name"]
        self.ID = self.shortTermData.data["id"]

        self.nutrition = Nutrition(self.age, self.weight, self.height, self.gender)
        goals = self.nutrition.AppropriateGoals()
        bmiGoals = self.nutrition.AppropriateGoalsBMI()
        acceptedGoals = []

        if goals[0] and bmiGoals[0]:
            acceptedGoals.append("calorie restriction")
        if goals[1] and bmiGoals[1]:
            acceptedGoals.append("sugar reduction")

        goalsString = "calorie restriction, and sugar reduction."
        if len(acceptedGoals) is 0:
            goalsString = acceptedGoals[0]

        statement = "Based on the information you provided, I believe the following goals are appropriate for you: "
        return statement + goalsString

    def ExplainGoalsStatement(self):
        calorieRestriction = "Calorie reduction refers to reducing your daily caloric intake by either choosing healthier foods, reducing portions, or simply eating less."
        sugarReduction = "Sugar reduction refers to reducing your daily sugar intake by eating foods with lower amounts of sugar, or simply reducing overall intake."
        return calorieRestriction + " " + sugarReduction

    def AskGoalsStatement(self):
        goals = self.nutrition.AppropriateGoals()
        bmiGoals = self.nutrition.AppropriateGoalsBMI()
        acceptedGoals = []

        goalString = ""

        if len(acceptedGoals) > 1:
            goalString = "The goals available to you are "
        else:
            goalString = "The only goal available to you is "

        for i in range(0, len(acceptedGoals)):
            if i is not len(acceptedGoals) - 1 and len(acceptedGoals) > 1:
                goalString = goalString + acceptedGoals[i]
                goalString = goalString + ", "
            elif i is not len(acceptedGoals) - 1 and len(acceptedGoals) is 1:
                goalString = goalString + acceptedGoals[i]
            elif i is len(acceptedGoals) - 1 and len(acceptedGoals) > 1:
                goalString = goalString + " and "
                goalString = goalString + acceptedGoals[i]
                goalString = goalString + "."
            elif i is len(acceptedGoals) - 1 and len(acceptedGoals) is 1:
                goalString = goalString + acceptedGoals[i]
                goalString = goalString + "."

        if len(acceptedGoals) > 1:
            if self.askedGoals:
                goals = "calorie restriction and sugar reduction."
                return "Which goal would you like to work on? " + goalString
            else:
                return "Which goal would you like to work on for the rest of our sessions?"
        else:
            #Since there is only one available goal, maybe asking the question is not that productive
            return "Which goal would you like to work on? " + goalString


    def AskGoalsResponse(self, response):
        nextState = "ConfirmGoal"
        decision = self.responseUtils.GetGoal(response)
        self.goal = decision
        return [], nextState

    def ConfirmGoalStatement(self, response):
        statement = "So the goal you chose is "
        goal = "calorie restriction"
        if self.goal is 0:
            goal = "calorie restriction"
        else:
            goal = "sugar reduction"

        return statement + goal + ". Is this correct?"

    def ConfirmGoalResponse(self, response):
        nextState = "AskGoals"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "AskGoals"
        else:
            self.shortTermData.writeData()
            nextState = "AskCurrentConsumption"

        return [], nextState

    def AskCurrentConsumptionStatement(self):
        goal = "calorie restriction"
        if self.goal is 0:
            goal = "How many calories have you consumed yesterday?"
        else:
            goal = "How many grams of sugar did you consume yesterday?"

        return goal

    def AskCurrentConsumptionResponse(self, response):
        nextState = 'AskCurrentConsumption'
        if self.goal is 0:
            numbers = self.responseUtils.GetNumber(response)
            if len(numbers) > 0:
                self.caloriesConsumed = numbers[0]
        else:
            numbers = self.responseUtils.GetNumber(response)
            if len(numbers) > 0:
                self.sugarConsumed = numbers[0]
        return [], nextState