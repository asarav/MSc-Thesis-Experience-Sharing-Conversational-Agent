#Look through all memory files
from os import listdir
from os.path import isfile, join

from data_retrieval.jsonManager import jsonManager
import pandas as pd

mypath = "../completed_sessions"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)

ids = []
prolificID = []
goalChanged = []
gender = []
age = []
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

milestoneDifference = []
goalDifference = []
goalDifferenceWithoutChange = []
day1Consumption = []
day2Consumption = []
day3Consumption = []


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

        if "prolificid" in fileData:
            prolificID.append(fileData["prolificid"])
        else:
            prolificID.append(None)

        gender.append(fileData["physicalData"]["gender"])
        age.append(fileData["physicalData"]["age"])

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

        if goal is 0:
            day1 = fileData["diet"]["session1"]["calories"]
            milestoneDifference.append((fileData["diet"]["session2"]["calories"] - fileData["milestone"])/day1)
            goalDifference.append((fileData["diet"]["session3"]["calories"] - fileData["finalGoal"])/day1)
            if "goalChanged" in fileData:
                if fileData["goalChanged"]:
                    goalDifferenceWithoutChange.append((fileData["diet"]["session3"]["calories"] - fileData["previousGoal"])/day1)
                else:
                    goalDifferenceWithoutChange.append((fileData["diet"]["session3"]["calories"] - fileData["finalGoal"])/day1)
            else:
                goalDifferenceWithoutChange.append((fileData["diet"]["session3"]["calories"] - fileData["finalGoal"])/day1)
            day1Consumption.append(day1)
            day2Consumption.append(fileData["diet"]["session2"]["calories"])
            day3Consumption.append(fileData["diet"]["session3"]["calories"])
        else:
            day1 = fileData["diet"]["session1"]["sugar"]
            milestoneDifference.append((fileData["diet"]["session2"]["sugar"] - fileData["milestone"])/day1)
            goalDifference.append((fileData["diet"]["session3"]["sugar"] - fileData["finalGoal"])/day1)
            if "goalChanged" in fileData:
                if fileData["goalChanged"]:
                    goalDifferenceWithoutChange.append((fileData["diet"]["session3"]["sugar"] - fileData["previousGoal"])/day1)
                else:
                    goalDifferenceWithoutChange.append((fileData["diet"]["session3"]["sugar"] - fileData["finalGoal"])/day1)
            else:
                goalDifferenceWithoutChange.append((fileData["diet"]["session3"]["sugar"] - fileData["finalGoal"])/day1)

            day1Consumption.append(day1)
            day2Consumption.append(fileData["diet"]["session2"]["sugar"])
            day3Consumption.append(fileData["diet"]["session3"]["sugar"])

        #Milestone adherence with goal change
        MA = 0
        zeroedMA = 0
        if goal is 0:
            day1 = fileData["diet"]["session1"]["calories"]
            milestone = fileData["milestone"]
            finalGoal = fileData["finalGoal"]
            MA = abs(milestone - fileData["diet"]["session2"]["calories"]) + abs(finalGoal - fileData["diet"]["session3"]["calories"])
            MA = MA/day1
            zeroedMD = milestone - fileData["diet"]["session2"]["calories"]
            zeroedFD = finalGoal - fileData["diet"]["session3"]["calories"]
            if zeroedMD > 0:
                zeroedMD = 0
            if zeroedFD > 0:
                zeroedFD = 0
            zeroedMA = abs(zeroedMD) + abs(zeroedFD)
            zeroedMA = zeroedMA/day1
        else:
            day1 = fileData["diet"]["session1"]["sugar"]
            milestone = fileData["milestone"]
            finalGoal = fileData["finalGoal"]
            MA = abs(milestone - fileData["diet"]["session2"]["sugar"]) + abs(finalGoal - fileData["diet"]["session3"]["sugar"])
            MA = MA/day1
            zeroedMD = milestone - fileData["diet"]["session2"]["sugar"]
            zeroedFD = finalGoal - fileData["diet"]["session3"]["sugar"]
            if zeroedMD > 0:
                zeroedMD = 0
            if zeroedFD > 0:
                zeroedFD = 0
            zeroedMA = abs(zeroedMD) + abs(zeroedFD)
            zeroedMA = zeroedMA/day1
        milestoneAdherence.append(MA)
        zeroedMilestoneAdherence.append(zeroedMA)

        #Milestone adherence without goal change
        MA = 0
        zeroedMA = 0
        if goal is 0:
            day1 = fileData["diet"]["session1"]["calories"]
            milestone = fileData["milestone"]
            finalGoal = fileData["finalGoal"]
            if "goalChanged" in fileData:
                if fileData["goalChanged"]:
                    finalGoal = fileData["previousGoal"]
            MA = abs(milestone - fileData["diet"]["session2"]["calories"]) + abs(finalGoal - fileData["diet"]["session3"]["calories"])
            MA = MA/day1
            zeroedMD = milestone - fileData["diet"]["session2"]["calories"]
            zeroedFD = finalGoal - fileData["diet"]["session3"]["calories"]
            if zeroedMD > 0:
                zeroedMD = 0
            if zeroedFD > 0:
                zeroedFD = 0
            zeroedMA = abs(zeroedMD) + abs(zeroedFD)
            zeroedMA = zeroedMA/day1
        else:
            day1 = fileData["diet"]["session1"]["sugar"]
            milestone = fileData["milestone"]
            finalGoal = fileData["finalGoal"]
            if "goalChanged" in fileData:
                if fileData["goalChanged"]:
                    finalGoal = fileData["previousGoal"]
            MA = abs(milestone - fileData["diet"]["session2"]["sugar"]) + abs(finalGoal - fileData["diet"]["session3"]["sugar"])
            MA = MA/day1
            zeroedMD = milestone - fileData["diet"]["session2"]["sugar"]
            zeroedFD = finalGoal - fileData["diet"]["session3"]["sugar"]
            if zeroedMD > 0:
                zeroedMD = 0
            if zeroedFD > 0:
                zeroedFD = 0
            zeroedMA = abs(zeroedMD) + abs(zeroedFD)
            zeroedMA = zeroedMA/day1
        milestoneAdherenceWithoutGoalChange.append(MA)
        zeroedMilestoneAdherenceWithoutGoalChange.append(zeroedMA)



dfConsent = pd.read_csv("surveys/Consent.csv")
dfQuestionnaire = pd.read_csv("surveys/Questionnaire.csv")

priorEfficacy = [None]*len(ids)

#Process consent form efficacy question
for index, row in dfConsent.iterrows():
    Consentid = row["Q1"].strip().upper()
    Consentid = Consentid.replace(" ", "")

    isProlific = False
    if len(Consentid) < 20:
        isProlific = False
    else:
        # Probably prolific
        isProlific = True

    #Find index of id
    index = 0
    try:
        if isProlific:
            index = prolificID.index(Consentid)
        else:
            index = ids.index(Consentid)
    except ValueError:
        print("Not Found Consent ", Consentid, isProlific)
        continue

    print(Consentid)
    print(index)
    priorEfficacy[index] = row["Q15"]

print("QUESTIONNAIRE")

education = [None]*len(ids)
fakeNatural = [None]*len(ids)
machineHuman = [None]*len(ids)
postEfficacy = [None]*len(ids)
efficacyChange = [None]*len(ids)
conscious = [None]*len(ids)
artificialLifelike = [None]*len(ids)
rigidElegant = [None]*len(ids)
deadAlive = [None]*len(ids)
stagnantLively = [None]*len(ids)
mechanicalOrganic = [None]*len(ids)
inertInteractive = [None]*len(ids)
apatheticResponsive = [None]*len(ids)
dislikeLike = [None]*len(ids)
unfriendlyFriendly = [None]*len(ids)
unkindKind = [None]*len(ids)
unpleasantPleasant = [None]*len(ids)
awfulNice = [None]*len(ids)
incompetentCompetent = [None]*len(ids)
ignorantKnowledgeable = [None]*len(ids)
irresponsibleResponsible = [None]*len(ids)
unintelligentIntelligent = [None]*len(ids)
foolishSensible = [None]*len(ids)
anxiousRelaxedBefore = [None]*len(ids)
agitatedCalmBefore = [None]*len(ids)
quiescentSurprisedBefore = [None]*len(ids)
anxiousRelaxedAfter = [None]*len(ids)
agitatedCalmAfter = [None]*len(ids)
quiescentSurprisedAfter = [None]*len(ids)
anxiousRelaxedChange = [None]*len(ids)
agitatedCalmChange = [None]*len(ids)
quiescentSurprisedChange = [None]*len(ids)
typeOfRelationship = [None]*len(ids)
usefulOrNotDiabetes = [None]*len(ids)
usefulOrNotObesity = [None]*len(ids)
convenience = [None]*len(ids)
preference = [None]*len(ids)
motivation = [None]*len(ids)
motivationBefore = [None]*len(ids)
motivationAfter = [None]*len(ids)
motivationBeforeDuringChange = [None]*len(ids)
motivationDuringAfterChange = [None]*len(ids)
diabetes = [None]*len(ids)
familyHistoryDiabetes = [None]*len(ids)
similarSystem = [None]*len(ids)
duration = [None]*len(ids)
numberOfSessions = [None]*len(ids)
understandingDiabetes = [None]*len(ids)
countryOfOrigin = [None]*len(ids)
engagement = [None]*len(ids)
autonomy = [None]*len(ids)
positiveNegative = [None]*len(ids)
firstTime = [None]*len(ids)

#Process questionnaire results
for index, row in dfQuestionnaire.iterrows():
    QuestionID = row["ID"].strip().upper()
    QuestionID = QuestionID.replace(" ", "")
    print(QuestionID)
    isProlific = False
    if len(QuestionID) < 20:
        isProlific = False
    else:
        # Probably prolific
        isProlific = True

    #Find index of id
    index = 0
    try:
        if isProlific:
            index = prolificID.index(QuestionID)
        else:
            index = ids.index(QuestionID)
    except ValueError:
        print("Not Found Questionnaire", QuestionID, isProlific)
        continue

    print(QuestionID)
    print(index)
    postEfficacy[index] = row["Efficacy"]
    efficacyChange[index] = int(postEfficacy[index]) - int(priorEfficacy[index])
    education[index] = row["Education Level"]
    machineHuman[index] = row["Machine or Human"]
    fakeNatural[index] = row["Fake or Natural"]
    conscious[index] = row["Unconsciousconscious"]
    artificialLifelike[index] = row["Artificiallifelike"]
    rigidElegant[index] = row["rigidlyelegantly"]
    deadAlive[index] = row["DeadAlive"]
    stagnantLively[index] = row["StagnantLively"]
    mechanicalOrganic[index] = row["MechanicalOrganic"]
    inertInteractive[index] = row["InertInteractive"]
    apatheticResponsive[index] = row["ApatheticResponsive"]
    dislikeLike[index] = row["DislikeLike"]
    unfriendlyFriendly[index] = row["UnfriendlyFriendly"]
    unkindKind[index] = row["UnkindKind"]
    unpleasantPleasant[index] = row["UnpleasantPleasant"]
    awfulNice[index] = row["AwfulNice"]
    incompetentCompetent[index] = row["IncompetentCompetent"]
    ignorantKnowledgeable[index] = row["IgnorantKnowledgeabl"]
    irresponsibleResponsible[index] = row["IrresponsibleRespons"]
    unintelligentIntelligent[index] = row["UnintelligentIntelli"]
    foolishSensible[index] = row["FoolishSensible"]
    #Before
    anxiousRelaxedBefore[index] = row["AnxiousRelaxed1"]
    agitatedCalmBefore[index] = row["AgitatedCalm1"]
    quiescentSurprisedBefore[index] = row["QuiescentSurprised1"]
    #After
    anxiousRelaxedAfter[index] = row["AnxiousRelaxed2"]
    agitatedCalmAfter[index] = row["AgitatedCalm2"]
    quiescentSurprisedAfter[index] = row["QuiescentSurprised2"]

    #Change
    anxiousRelaxedChange[index] = int(row["AnxiousRelaxed2"]) - int(row["AnxiousRelaxed1"])
    agitatedCalmChange[index] = int(row["AgitatedCalm2"]) - int(row["AgitatedCalm1"])
    quiescentSurprisedChange[index] = int(row["QuiescentSurprised2"]) - int(row["QuiescentSurprised1"])

    typeOfRelationship[index] = row["TypeOfRelationship"]

    usefulOrNotDiabetes[index] = row["UsefulOrNot"]
    usefulOrNotObesity[index] = row["UsefulOrNotObesity"]
    convenience[index] = row["Convenience"]
    preference[index] = row["Preference"]

    motivationBefore[index] = row["MotivationBefore"]
    motivation[index] = row["Motivation"]
    motivationAfter[index] = row["MotivationAfter"]
    motivationBeforeDuringChange[index] = int(row["Motivation"]) - int(row["MotivationBefore"])
    motivationDuringAfterChange[index] = int(row["MotivationAfter"]) - int(row["Motivation"])

    engagement[index] = row["Engagement"]
    autonomy[index] = row["Autonomy"]
    positiveNegative[index] = row["PositiveNegative"]

    diabetes[index] = row["Diabetes"]

    firstTime[index] = row["FirstTime"]
    familyHistoryDiabetes[index] = row["FamilyHistory"]
    similarSystem[index] = row["SimilarSystem"]

    duration[index] = row["Duration"]

    numberOfSessions[index] = row["Number of Sessions"]
    understandingDiabetes[index] = row["Understanding"]

    countryOfOrigin[index] = row["Country of Origin"]


columnContents = list(zip(ids,
                   conditions,
                   goals,
                   gender,
                   age,
                   countryOfOrigin,
                   milestoneAchievement,
                   finalGoalAchievement,
                   finalGoalAchievementWithoutGoalChange,
                          agreementPercentageExperiences,
                          futureWork,
                          milestoneAdherence,
                          zeroedMilestoneAdherence,
                          milestoneAdherenceWithoutGoalChange,
                          zeroedMilestoneAdherenceWithoutGoalChange,
                          milestoneDifference,
                          goalDifference,
                          goalDifferenceWithoutChange,
                          day1Consumption,
                          day2Consumption,
                          day3Consumption,
                          priorEfficacy,
                          postEfficacy,
                          efficacyChange,
                          education,
                          fakeNatural,
                          machineHuman,
                          conscious,
                          artificialLifelike,
                          rigidElegant,
                          deadAlive,
                          stagnantLively,
                          mechanicalOrganic,
                          inertInteractive,
                          apatheticResponsive,
                          dislikeLike,
                          unfriendlyFriendly,
                          unkindKind,
                          unpleasantPleasant,
                          awfulNice,
                          incompetentCompetent,
                          ignorantKnowledgeable,
                          irresponsibleResponsible,
                          unintelligentIntelligent,
                          foolishSensible,
                          anxiousRelaxedBefore,
                          agitatedCalmBefore,
                          quiescentSurprisedBefore,
                          anxiousRelaxedAfter,
                          agitatedCalmAfter,
                          quiescentSurprisedAfter,
                          anxiousRelaxedChange,
                          agitatedCalmChange,
                          quiescentSurprisedChange,
                          typeOfRelationship,
                          usefulOrNotDiabetes,
                          usefulOrNotObesity,
                          convenience,
                          preference,
                          motivationBefore,
                          motivation,
                          motivationAfter,
                          motivationBeforeDuringChange,
                          motivationDuringAfterChange,
                          engagement,
                          autonomy,
                          positiveNegative,
                          diabetes,
                          firstTime,
                          familyHistoryDiabetes,
                          similarSystem,
                          duration,
                          numberOfSessions,
                          understandingDiabetes))
columnNames = ['id',
               'condition',
               'goals',
               'gender',
               'age',
               'countryOfOrigin',
               'milestoneAchievement',
               'finalGoalAchievement',
               'finalGoalAchievementWithoutGoalChange',
               'agreementPercentage',
               'futureWork',
               'milestoneAdherence',
               'zeroedMilestoneAdherence',
               'milestoneAdherenceWithoutGoalChange',
               'zeroedMilestoneAdherenceWithoutGoalChange',
               'milestoneDifference',
               'goalDifference',
               'goalDifferenceWithoutChange',
               'day1Consumption',
               'day2Consumption',
               'day3Consumption',
               'priorEfficacy',
               'postEfficacy',
               'efficacyChange',
               'education',
               'fakeNatural',
               'machineHuman',
               'consciousUnconscious',
               'artificialLifelike',
               'rigidElegant',
               'deadAlive',
               'stagnantLively',
               'mechanicalOrganic',
               'inertInteractive',
               'apatheticResponsive',
               'dislikeLike',
               'unfriendlyFriendly',
               'unkindKind',
               'unpleasantPleasant',
               'awfulNice',
               'incompetentCompetent',
               'ignorantKnowledgeable',
               'irresponsibleResponsible',
               'unintelligentIntelligent',
               'foolishSensible',
               'anxiousRelaxedBefore',
               'agitatedCalmBefore',
               'quiescentSurprisedBefore',
               'anxiousRelaxedAfter',
               'agitatedCalmAfter',
               'quiescentSurprisedAfter',
               'anxiousRelaxedChange',
               'agitatedCalmChange',
               'quiescentSurprisedChange',
               'typeOfRelationship',
               'usefulOrNotDiabetes',
               'usefulOrNotObesity',
               'convenience',
               'preference',
               'motivationBefore',
               'motivation',
               'motivationAfter',
               'motivationBeforeDuringChange',
               'motivationDuringAfterChange',
               'engagement',
               'autonomy',
               'positiveNegative',
               'diabetes',
               'firstTime',
               'familyHistoryDiabetes',
               'similarSystem',
               'duration',
               'numberOfSessions',
               'understandingDiabetes']

dfJson = pd.DataFrame(columnContents,
                  columns =columnNames)

dfJson.to_csv("output_files/summary.csv", index=False)

condition1 = dfJson.loc[dfJson['condition'] == 0]
condition2 = dfJson.loc[dfJson['condition'] == 1]
condition3 = dfJson.loc[dfJson['condition'] == 2]

condition1.to_csv("output_files/summary_1.csv", index=False)
condition2.to_csv("output_files/summary_2.csv", index=False)
condition3.to_csv("output_files/summary_3.csv", index=False)