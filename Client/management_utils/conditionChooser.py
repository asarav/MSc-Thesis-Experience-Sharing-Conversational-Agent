#Chooses a condition for the user
from os import listdir
from os.path import isfile, join

from data_retrieval.jsonManager import jsonManager

class ConditionChooser:
    def __init__(self):
        print("Initialized Condition Chooser")

    def getCondition(self):
        #Iterate through all files except the session file to get a total count of all three conditions.
        conditions = [0, 0, 0]
        # Look through all memory files
        mypath = "../interaction_data"
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        print(onlyfiles)

        for file in onlyfiles:
            print(file)
            manager = jsonManager()
            manager.readJSON(mypath + "/" + file)
            fileData = manager.data

            if "condition" in fileData:
                print("Condition Found")
            else:
                print("Condition Not Found")

        # Choose the condition where the number of users is the lowest (0 to 2).
        min = -1
        chosenCondition = 0
        for i in range(0, len(conditions)):
            if conditions[i] < min:
                print("Found Min")

        return