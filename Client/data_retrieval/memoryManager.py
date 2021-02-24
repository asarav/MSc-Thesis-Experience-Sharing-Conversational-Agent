import random

import data_retrieval.jsonManager as jsonManager

#A wrapper for the jsonManager that is used for accessing interaction data in different flows.
class MemoryManager:
    def __init__(self):
        # READING
        # Opening JSON file
        self.data = {}
        self.jsonLoaded = False
        self.jsonSaved = False
        self.fileName = "interaction_data/session.json"
        self.jsonManager = jsonManager.jsonManager()

    #Used to read data for the first time.
    def readData(self):
        fileExists = self.jsonManager.readJSON(self.fileName)
        self.data = self.jsonManager.data
        self.jsonLoaded = True

    #Used to save data before going to another flow
    def writeData(self):
        self.jsonManager.writeJSON(self.data, self.fileName)
        self.jsonSaved = True

    def readDataFromLongTermMemory(self, id):
        fileExists = self.jsonManager.readJSON("interaction_data/" + id + ".json")
        self.data = self.jsonManager.data
        self.jsonLoaded = True
        return fileExists

    def writeDataToLongTermMemory(self, id):
        self.jsonManager.writeJSON(self.data, "interaction_data/" + id + ".json")
        self.jsonSaved = True

    #Type refers to praise (0) or criticism (1)
    def chooseMemory(self, session=1, type=0):
        experiences = self.data["experiences"]

        notFound = True
        chosenExperience = 0

        #For condition 2, choose a memory that has not already been used.
        #For condition 1, choose a memory that has already been used. If there is not a memory that has been used, use any memory.

        while notFound:
            chosenExperience = random.choice(range(0, len(experiences)))
            #Ensure that the experience is from a proper session.
            if self.data["experiences"][chosenExperience]["session"] is session:
                notFound = False

        #Set the data as used and save it just in case
        self.data["experiences"][chosenExperience]["used"] = True
        self.writeData()

        if type is 0:
            chosenPhrase = random.choice(range(0, len(experiences[chosenExperience]["praise"])))
            return self.data["experiences"][chosenExperience]["praise"][chosenPhrase]
        else:
            chosenPhrase = random.choice(range(0, len(experiences[chosenExperience]["criticism"])))
            return self.data["experiences"][chosenExperience]["criticism"][chosenPhrase]
