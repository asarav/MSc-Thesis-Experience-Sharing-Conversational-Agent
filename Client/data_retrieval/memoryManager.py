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