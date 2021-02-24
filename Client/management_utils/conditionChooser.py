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
            if file == "session.json":
                continue
            print(file)
            manager = jsonManager()
            manager.readJSON(mypath + "/" + file)
            fileData = manager.data

            if "condition" in fileData:
                conditions[fileData["condition"]] = conditions[fileData["condition"]] + 1
            else:
                print("Condition Not Found")

        # Choose the condition where the number of users is the lowest (0 to 2).
        print(conditions)
        min = conditions[0]
        chosenCondition = 0
        for i in range(1, len(conditions)):
            if conditions[i] < min:
                chosenCondition = i
                min = conditions[i]

        print("Chosen Condition ", chosenCondition)
        return chosenCondition
