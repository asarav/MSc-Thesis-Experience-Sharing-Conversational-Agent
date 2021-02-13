import management_utils.response_manager as ResponseManager
import management_utils.search_based_conversation as SBC
import data_retrieval.memoryManager as shortTermData
import management_utils.diabetesConversation as diabetesConversation
from management_utils import calorieRestrictionConversation, sugarRestrictionConversation, struggleConversation


class Session2QuestionsAndEnd:
    def __init__(self):
        self.responseUtils = ResponseManager.ResponseManager()
        self.calorieRestrictionAnswers = SBC.SearchBasedConversation(calorieRestrictionConversation.conversation, "Calorie Restriction Questions")
        self.sugarReductionAnswers = SBC.SearchBasedConversation(sugarRestrictionConversation.conversation, "Sugar Reduction Questions")
        self.struggleAnswers = SBC.SearchBasedConversation(struggleConversation.conversation, "Struggle Questions", False)
        self.ID = "1234"
        self.username = ""
        self.firstTimeActivitiesQuestion = True
        self.gender = 0
        self.age = 18
        self.weight = 60
        self.height = 160

        #Load user data
        self.shortTermData = shortTermData.MemoryManager()
        self.shortTermData.data["session"] = 1

        self.states = [
        {
            "name": "AskStruggle",
            "statement": self.AskStruggleStatement,
            "response": self.AskStruggleResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "AskOtherOpinions",
            "statement": "How do you think your family, friends or coworkers would react if they heard about you reaching your goal?",
            "response": self.AskOtherOpinionsResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ContinueAndTips",
            "statement": self.ContinueAndTipsStatement,
            "response": "QuestionsAboutActivities",
            "stateType": "Statement"
        },
        {
            "name": "QuestionsAboutActivities",
            "statement": self.QuestionsAboutActivitiesStatement,
            "response": self.QuestionsAboutActivitiesResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "AskQuestionsAboutActivities",
            "statement": "What is your question?",
            "response": self.AskActivitiesQuestionResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ActivitiesAnswer",
            "statement": self.ProvideActivitiesAnswer,
            "response": "QuestionsAboutActivities",
            "stateType": "Statement"
        },
        {
            "name": "ReviewGoalsSession2",
            "statement": self.ReviewGoalsSession2Statement,
            "response": self.ReviewGoalsSession2Response,
            "stateType": "AnswerResponse"
        },
        {
            "name": "ExplainGoalsSession2",
            "statement": self.ExplainGoalsSession2Statement,
            "response": "GoodbyeSession2",
            "stateType": "Statement"
        },
        {
            "name": "GoodbyeSession2",
            "statement": "I will see you in the final session. Work hard and good luck on your diet. Bye.",
            "response": "",
            "stateType": "End"
        }
        ]

    def AskStruggleStatement(self):
        #Load the data here because it is the first statement.
        self.shortTermData.readData()
        self.ID = self.shortTermData.data["id"]
        self.username = self.shortTermData.data["name"]
        self.goal = self.shortTermData.data["goal"]
        self.finalGoal = self.shortTermData.data["finalGoal"]
        self.milestone = self.shortTermData.data["milestone"]
        return "What are you struggling with?"

    def AskStruggleResponse(self, response):
        nextState = "AskOtherOpinions"
        #Save everything to the file
        self.struggle = response
        self.shortTermData.data["experiences"].append({
            "Question": "What are you struggling with?",
            "Answer": response,
            "session": 2
        })
        return [], nextState

    def AskOtherOpinionsResponse(self, response):
        nextState = "ContinueAndTips"
        #Save everything to the file
        self.struggle = response
        self.shortTermData.data["experiences"].append({
            "Question": "How do you think your family, friends or coworkers would react if they heard about you reaching your goal?",
            "Answer": response,
            "session": 2
        })

        self.getStruggleAdvice = self.struggleAnswers.askQuestion(response)
        return [], nextState

    def ContinueAndTipsStatement(self):
        statement = "Let's continue. Our next session is our last, so that means that you will be trying to achieve your final goal of "
        if self.finalGoal is 0:
            newCalories = self.shortTermData.data["session2Progress"]["calories"]
            statement = statement + str(self.finalGoal) + " calories before we meet."
            statement = statement + " This means you have " + str(newCalories - self.finalGoal) + " calories left to reach your goal."
        else:
            newSugar = self.shortTermData.data["session2Progress"]["sugar"]
            statement = statement + str(self.finalGoal) + " grams of sugar before we meet."
            statement = statement + " This means you have " + str(newSugar - self.finalGoal) + " grams of sugar left to reach your goal."

        #Add some tips and strategies based on the struggles of the user
        statement = statement + " For your diet, if you are not trying to remove food items, maybe try to focus on whole foods and complex carbohydrates such as beans, grains, and starchy vegetables. Pass on the simple sugars, like those in processed baked goods. Those can raise blood sugar without providing wholesome nutrition."

        statement = statement + " Regarding your struggles, I think I can offer some advice. "

        statement = statement + self.getStruggleAdvice

        return statement

    def QuestionsAboutActivitiesStatement(self):
        statement = ""
        if self.firstTimeActivitiesQuestion:
            statement = "Do you have any questions about what to do to reach your goal?"
        else:
            statement = "Do you have any other questions?"
        return statement

    def QuestionsAboutActivitiesResponse(self, response):
        nextState = ""
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "ReviewGoalsSession2"
        else:
            nextState = "AskQuestionsAboutActivities"

        return [], nextState

    def AskActivitiesQuestionResponse(self, response):
        nextState = "ActivitiesAnswer"
        self.ActivitiesQuestionAnswer = ""
        if self.goal is 0:
            self.ActivitiesQuestionAnswer = self.calorieRestrictionAnswers.askQuestion(response)
        else:
            self.ActivitiesQuestionAnswer = self.sugarReductionAnswers.askQuestion(response)
        return [], nextState

    def ProvideActivitiesAnswer(self):
        return self.ActivitiesQuestionAnswer

    def ReviewGoalsSession2Statement(self):
        statement = "Great. Only one more session left and we will see if you reach your goal or not. It won't be easy, but I believe you will get there."
        statement = statement + " Your final goal is "
        if self.goal is 0:
            statement = statement + str(self.finalGoal) + " maximum calories in your daily intake."
        else:
            statement = statement + str(self.finalGoal) + " maximum grams of sugar in your daily intake."
        statement = statement + " Does that make sense?"
        return statement

    def ReviewGoalsSession2Response(self, response):
        nextState = ""
        decision = self.responseUtils.YesOrNo(response)
        if decision is 0:
            nextState = "ExplainGoalsSession2"
        else:
            nextState = "GoodbyeSession2"
        self.shortTermData.data["session"] = 3
        self.shortTermData.writeData()
        self.shortTermData.writeDataToLongTermMemory(self.shortTermData.data["id"])
        return [], nextState

    def ExplainGoalsSession2Statement(self):
        statement = "Your final goal is "
        if self.goal is 0:
            statement = statement + str(self.finalGoal) + " calories. This means you should reduce some of the food items you are eating, or choose healthier alternatives with fewer calories."
        else:
            statement = statement + str(self.finalGoal) + " grams of sugar. This means you should reduce some of the food items you are eating that have high levels of sugar, or choose healthier alternatives with fewer grams of sugar."
        return statement