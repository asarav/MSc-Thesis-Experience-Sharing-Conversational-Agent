#Look through all memory files
from os import listdir
from os.path import isfile, join

from data_retrieval.jsonManager import jsonManager
import pandas as pd

mypath = "../trial_runs"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)

ids = []
prolificID = []
goalChanged = []
gender = []
milestoneAchievement = []
finalGoalAchievement = []
finalGoalAchievementWithoutGoalChange = []
conditions = []
agreementPercentageExperiences = []
futureWork = []
goals = []
milestoneAdherence = []
zeroedMilestoneAdherence = []
milestoneAdherenceWithoutGoalChange = []
zeroedMilestoneAdherenceWithoutGoalChange = []

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
        condition = fileData["condition"]
        conditions.append(fileData["condition"])
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

        if condition is 1 or condition is 2:
            if "ExperienceResponse" in fileData:
                total = 0
                agreements = 0
                for item in fileData["ExperienceResponse"]:
                    total = total + 1
                    if item["agree"] is 1:
                        agreements = agreements + 1
                if total is 0:
                    agreementPercentageExperiences.append(0)
                else:
                    agreementPercentageExperiences.append(agreements/total)
            else:
                agreementPercentageExperiences.append(0)
        else:
            agreementPercentageExperiences.append(0)

        if "FutureWork" in fileData:
            if fileData["FutureWork"][0]["agree"] is 1:
                futureWork.append(True)
            else:
                futureWork.append(False)
        else:
            futureWork.append(False)

        #Milestone adherence with goal change
        MA = 0
        zeroedMA = 0
        if goal is 0:
            milestone = fileData["milestone"]
            finalGoal = fileData["finalGoal"]
            MA = abs(milestone - fileData["diet"]["session2"]["calories"]) + abs(finalGoal - fileData["diet"]["session3"]["calories"])
            zeroedMD = milestone - fileData["diet"]["session2"]["calories"]
            zeroedFD = finalGoal - fileData["diet"]["session3"]["calories"]
            if zeroedMD > 0:
                zeroedMD = 0
            if zeroedFD > 0:
                zeroedFD = 0
            zeroedMA = abs(zeroedMD) + abs(zeroedFD)
        else:
            milestone = fileData["milestone"]
            finalGoal = fileData["finalGoal"]
            MA = abs(milestone - fileData["diet"]["session2"]["sugar"]) + abs(finalGoal - fileData["diet"]["session3"]["sugar"])
            zeroedMD = milestone - fileData["diet"]["session2"]["sugar"]
            zeroedFD = finalGoal - fileData["diet"]["session3"]["sugar"]
            if zeroedMD > 0:
                zeroedMD = 0
            if zeroedFD > 0:
                zeroedFD = 0
            zeroedMA = abs(zeroedMD) + abs(zeroedFD)
        milestoneAdherence.append(MA)
        zeroedMilestoneAdherence.append(zeroedMA)

        #Milestone adherence without goal change
        MA = 0
        zeroedMA = 0
        if goal is 0:
            milestone = fileData["milestone"]
            finalGoal = fileData["finalGoal"]
            if "goalChanged" in fileData:
                if fileData["goalChanged"]:
                    finalGoal = fileData["previousGoal"]
            MA = abs(milestone - fileData["diet"]["session2"]["calories"]) + abs(finalGoal - fileData["diet"]["session3"]["calories"])
            zeroedMD = milestone - fileData["diet"]["session2"]["calories"]
            zeroedFD = finalGoal - fileData["diet"]["session3"]["calories"]
            if zeroedMD > 0:
                zeroedMD = 0
            if zeroedFD > 0:
                zeroedFD = 0
            zeroedMA = abs(zeroedMD) + abs(zeroedFD)
        else:
            milestone = fileData["milestone"]
            finalGoal = fileData["finalGoal"]
            if "goalChanged" in fileData:
                if fileData["goalChanged"]:
                    finalGoal = fileData["previousGoal"]
            MA = abs(milestone - fileData["diet"]["session2"]["sugar"]) + abs(finalGoal - fileData["diet"]["session3"]["sugar"])
            zeroedMD = milestone - fileData["diet"]["session2"]["sugar"]
            zeroedFD = finalGoal - fileData["diet"]["session3"]["sugar"]
            if zeroedMD > 0:
                zeroedMD = 0
            if zeroedFD > 0:
                zeroedFD = 0
            zeroedMA = abs(zeroedMD) + abs(zeroedFD)
        milestoneAdherenceWithoutGoalChange.append(MA)
        zeroedMilestoneAdherenceWithoutGoalChange.append(zeroedMA)


df = pd.DataFrame(list(zip(ids, conditions, goals, milestoneAchievement, finalGoalAchievement, finalGoalAchievementWithoutGoalChange, agreementPercentageExperiences, futureWork, milestoneAdherence, zeroedMilestoneAdherence, milestoneAdherenceWithoutGoalChange, zeroedMilestoneAdherenceWithoutGoalChange)),
                  columns =['id', 'condition', 'goals', 'milestoneAchievement', 'finalGoalAchievement', 'finalGoalAchievementWithoutGoalChange', 'agreementPercentage', 'futureWork', 'milestoneAdherence', 'zeroedMilestoneAdherence', 'milestoneAdherenceWithoutGoalChange', 'zeroedMilestoneAdherenceWithoutGoalChange'])


df.to_csv("output_files/summary.csv", index=False)