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
    def chooseMemory(self, session=1, type=0, condition=2):
        experiences = self.data["experiences"]

        notFound = True
        chosenExperience = 0

        #For condition 1, choose a memory that has already been used. If there is not a memory that has been used, use any memory.
        if condition is 1:
            #Find a memory that has been used. Only refer to session 1 memories to avoid variation
            for i in range(0, len(self.data["experiences"])):
                if self.data["experiences"][i]["session"] is 1:
                    if "used" in self.data["experiences"][i]:
                        if self.data["experiences"][i]["used"]:
                            chosenExperience = i
                            notFound = False

            #If a memory has not been used, just choose one from session 1
            if notFound:
                while notFound:
                    chosenExperience = random.choice(range(0, len(experiences)))
                    # Ensure that the experience is from the proper session and not used.
                    if self.data["experiences"][chosenExperience]["session"] is 1:
                        notFound = False
        #For condition 2, choose a memory that has not already been used.
        elif condition is 2:
            #Find a memory that has not been used
            while notFound:
                chosenExperience = random.choice(range(0, len(experiences)))
                # Ensure that the experience is from the proper session and not used.
                if self.data["experiences"][chosenExperience]["session"] is session:
                    if "used" not in self.data["experiences"][chosenExperience]:
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
