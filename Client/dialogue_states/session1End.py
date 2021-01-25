import management_utils.response_manager as ResponseManager
import management_utils.search_based_conversation as SBC
import data_retrieval.shortTermData as shortTermData
from diet_utils.mileStone import MileStone
from diet_utils.nutrition import Nutrition


class Session1End:
    def __init__(self):
        self.responseUtils = ResponseManager.ResponseManager()
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

        #Load user data
        self.shortTermData = shortTermData.ShortTermData()
        self.dataLoaded = False

        self.states = [
        {
            "name": "ExplainIntermediateMilestone",
            "statement": "Do you have any questions on how to reach this milestone or any strategies?",
            "response": "ExplainIntermediateMilestoneResponse",
            "stateType": "Statement"
        }
        ]

    def ExplainIntermediateMilestoneResponse(self, response):
        #Load the data here because it is the first statement.
        if self.dataLoaded is False:
            self.shortTermData.readData()
            #Load all the physical data into the class members
            physicalData = self.shortTermData.data["physicalData"]
            self.gender = physicalData["gender"]
            self.age = physicalData["age"]
            self.weight = physicalData["age"]
            self.height = physicalData["age"]
            self.username = self.shortTermData.data["name"]
            self.ID = self.shortTermData.data["id"]
            self.goal = self.shortTermData.data["goal"]

            self.dataLoaded = True

        nextState = ""


        return [], nextState