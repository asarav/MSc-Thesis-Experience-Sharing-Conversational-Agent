#Look through all memory files
from os import listdir
from os.path import isfile, join

from data_retrieval.jsonManager import jsonManager
import pandas as pd

mypath = "../trial_runs"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)

ids = []
milestoneAchievement = []
finalGoalAchievement = []
finalGoalAchievementWithoutGoalChange = []
condition = []
agreementPercentage = []
goals = []

for file in onlyfiles:
    if file == "session.json":
        continue
    manager = jsonManager()
    manager.readJSON(mypath + "/" + file)
    fileData = manager.data
    if fileData["session"] is 4:
        print(file)
        id = fileData["id"]
        ids.append(id)
        #Milestone achievement
        condition.append(fileData["condition"])
        milestoneAchievement.append(fileData["diet"]["session2"]["progressSufficient"])
        #Final Goal Achievement
        finalGoalAchievement.append(fileData["diet"]["session3"]["progressSufficient"])
        #Goal Type
        goal = fileData["goal"]
        goals.append(goal)
        #Final Goal Achievement without Goal change
        if "goalChanged" in fileData:
            if fileData["goalChanged"]:
                #Determine if it is a more ambitious goal or less ambitious goal
                previousGoal = fileData["previousGoal"]
                finalGoal = fileData["finalGoal"]
                moreAmbitious = False
                if previousGoal >= finalGoal:
                    moreAmbitious = True
                # This means they still achieved their goal despite it being more ambitious.
                if moreAmbitious:
                    finalGoalAchievementWithoutGoalChange.append(fileData["diet"]["session3"]["progressSufficient"])
                else:
                    #When it is less ambitious
                    if goal is 0:
                        consumption = fileData["diet"]["session3"]["calories"]
                        if consumption < fileData["previousGoal"]:
                            finalGoalAchievementWithoutGoalChange.append(True)
                        else:
                            finalGoalAchievementWithoutGoalChange.append(False)
                    else:
                        consumption = fileData["diet"]["session3"]["sugar"]
        else:
            finalGoalAchievementWithoutGoalChange.append(fileData["diet"]["session3"]["progressSufficient"])

df = pd.DataFrame(list(zip(ids, condition, goals, milestoneAchievement, finalGoalAchievement, finalGoalAchievementWithoutGoalChange)),
                  columns =['id', 'condition', 'goals', 'milestoneAchievement', 'finalGoalAchievement', 'finalGoalAchievementWithoutGoalChange'])
df.to_csv("output_files/summary.csv")