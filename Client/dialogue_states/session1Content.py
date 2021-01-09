import management_utils.response_manager as ResponseManager
import management_utils.search_based_conversation as SBC

class Session1Content:
    def __init__(self):
        self.responseUtils = ResponseManager.ResponseManager()
        self.DiabetesAnswers = SBC.SearchBasedConversation([], "Diabetes Questions")
        self.username = ""
        self.firstTimeDiabetesQuestion = True
        self.gender = 0
        self.age = 18
        self.weight = 60
        self.height = 160
        self.askedGoals = False
        self.goal = 0
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
            "response": "AnswerDiabetesQuestions",
            "stateType": "Statement"
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
            "statement": "There are three goals that you can choose. These are calorie restriction, sugar reduction and diet composition change. Before we choose a goal, I would like to ask you for a few personal details so that we can ensure that the goal that is chosen is appropriate for you.",
            "response": "ListGoals",
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
        },
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
        }
        ]

    def GetStartedGreetingStatement(self):
        return "Great. Nice to meet you " + self.username + ". Let's start improving your diet"

    def AnswerDiabetesQuestionsResponse(self, response):
        nextState = "AskDiabetesQuestion"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "ListGoals"
        else:
            nextState = "AskDiabetesQuestion"
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
        return "Your gender is " + self.gender + ". Is this correct?"

    def ConfirmGenderResponse(self, response):
        nextState = "AskGender"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "AskGender"
        else:
            nextState = "AskAge"
        return [], nextState

    def AskAgeResponse(self, response):
        nextState = "ConfirmAge"
        numbers = self.responseUtils.GetNumber(response)
        if len(numbers) > 1:
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
            nextState = "AskWeight"
        return [], nextState

    def AskWeightResponse(self, response):
        nextState = "ConfirmWeight"
        numbers = self.responseUtils.GetNumber(response)
        if len(numbers) > 1:
            self.weight = numbers[0]
        return [], nextState

    def ConfirmWeightStatement(self):
        return "You weight is " + str(self.weight) + " kilograms. Is this correct?"

    def ConfirmWeightResponse(self, response):
        nextState = "AskWeight"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "AskWeight"
        else:
            nextState = "AskHeight"
        return [], nextState

    def AskHeightResponse(self, response):
        nextState = "ConfirmHeight"
        numbers = self.responseUtils.GetNumber(response)
        if len(numbers) > 1:
            self.height = numbers[0]
        return [], nextState

    def ConfirmHeightStatement(self, response):
        return "Your height is " + str(self.height) + " centimeters. Is that correct?"

    def ConfirmHeightResponse(self, response):
        nextState = "AskHeight"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "AskHeight"
        else:
            nextState = "ListGoals2"
        return [], nextState

    def ListGoals2Statement(self):
        statement = "Based on the information you provided, I believe the following goals are appropriate for you: "
        goals = "calorie restriction, sugar reduction and diet composition change."
        return statement + goals

    def ExplainGoalsStatement(self):
        calorieRestriction = "Calorie reduction refers to reducing your daily caloric intake by either choosing healthier foods, reducing portions, or simply eating less."
        sugarReduction = "Sugar reduction refers to reducing your daily sugar intake by eating foods with lower amounts of sugar, or simply reducing overall intake."
        dietCompositionChange = "Diet composition change refers to the food groups you are eating from. The point of this goal is to "
        return calorieRestriction + " " + sugarReduction + " " + dietCompositionChange

    def AskGoalsStatement(self):
        if self.askedGoals:
            goals = "calorie restriction, sugar reduction and diet composition change."
            return "Which goal would you like to work on? The goals available to you are " + goals
        else:
            return "Which goal would you like to work on for the rest of our sessions?"


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
        elif self.goal is 1:
            goal = "sugar reduction"
        else:
            goal = "diet composition change"

        return statement + goal + ". Is this correct?"

    def ConfirmGoalResponse(self, response):
        nextState = "AskGoals"
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "AskGoals"
        else:
            nextState = "???????"

