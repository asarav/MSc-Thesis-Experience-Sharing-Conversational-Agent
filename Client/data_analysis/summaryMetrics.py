from statistics import mean, stdev

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plotHistogram(valueList, binsNum, label="None"):
    plt.hist(valueList, bins=binsNum, alpha=0.5, label=label, edgecolor='black')

def efficacyHistogram(data, title="User Efficacy"):
    plotHistogram(data["priorEfficacy"].tolist(), 5, "Prior")
    plotHistogram(data["postEfficacy"].tolist(), 5, "Post")
    plt.legend(loc='upper right')
    plt.title(title)
    plt.show()
    print("Prior Efficacy", data["priorEfficacy"].mean(), data["priorEfficacy"].std())
    print("Post Efficacy", data["postEfficacy"].mean(), data["postEfficacy"].std())

def efficacyDifference(data, title="User Efficacy Difference"):
    prior = data["priorEfficacy"].tolist()
    post = data["postEfficacy"].tolist()
    diff = []
    for i in range(0, len(prior)):
        diff.append(post[i] - prior[i])
    plotHistogram(diff, 5)
    plt.title(title)
    plt.show()
    print("Efficacy Difference", np.mean(diff), np.std(diff))

def genderHistogram(data, title="Participants by Gender"):
    genders = data["gender"].tolist()

    plotHistogram(genders, 3)
    plt.title(title)
    plt.show()

def ageHistogram(data, title="Participants by Age"):
    age = data["age"].tolist()

    plotHistogram(age, 10)
    plt.title(title)
    plt.show()

def firstTimeInteractingHistogram(data, title="First Time Interacting with Robot"):
    genders = data["firstTime"].tolist()

    plotHistogram(genders, 2)
    plt.title(title)
    plt.show()

def diabetesHistogram(data, title="Has Diabetes"):
    genders = data["diabetes"].tolist()

    plotHistogram(genders, 2)
    plt.title(title)
    plt.show()

def familyHistoryHistogram(data, title="Family History"):
    genders = data["familyHistoryDiabetes"].tolist()

    plotHistogram(genders, 2)
    plt.title(title)
    plt.show()

def similarSystemHistogram(data, title="Would use Similar System for other Health Goals"):
    genders = data["similarSystem"].tolist()

    plotHistogram(genders, 2)
    plt.title(title)
    plt.show()

def subcategorybar(X, vals, width=0.8):
    n = len(vals)
    _X = np.arange(len(X))
    for i in range(n):
        plt.bar(_X - width/2. + i/float(n)*width, vals[i],
                width=width/float(n), align="edge")
    plt.xticks(_X, X)

def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = round(rect.get_height(), 1)
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def getAnthropomorphism(data):
    fakeNatural = data["fakeNatural"].mean()
    machineHuman = data["machineHuman"].mean()
    consciousUnconscious = data["consciousUnconscious"].mean()
    artificialLifelike = data["artificialLifelike"].mean()
    rigidElegant = data["rigidElegant"].mean()

    return [fakeNatural, machineHuman, consciousUnconscious, artificialLifelike, rigidElegant],\
           [data["fakeNatural"].std(), data["machineHuman"].std(), data["consciousUnconscious"].std(), data["artificialLifelike"].std(), data["rigidElegant"].std()]

def anthropomorphismBarChart(data, data_std, labels):
    length = len(data)
    x_labels = labels

    # Set plot parameters
    fig, ax = plt.subplots()
    width = 0.1  # width of bar
    x = np.arange(length)

    print(x)
    print(data[:, 0])
    rects1 = ax.bar(x, data[:, 0], width, color='green', label='Fake Natural', yerr=data_std[:, 0])
    rects2 = ax.bar(x + width, data[:, 1], width, color='#0F52BA', label='Machine Human', yerr=data_std[:, 1])
    rects3 = ax.bar(x + (2 * width), data[:, 2], width, color='#6593F5', label='Conscious Unconscious', yerr=data_std[:, 2])
    rects4 = ax.bar(x + (3 * width), data[:, 3], width, color='#73C2FB', label='Artificial Lifelike', yerr=data_std[:, 3])
    rects5 = ax.bar(x + (4 * width), data[:, 4], width, color='red', label='Rigid Elegant', yerr=data_std[:, 4])

    ax.set_ylabel('Likert Item Value')
    ax.set_ylim(0, 6)
    ax.set_xticks(x + width + width / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Conditions')
    ax.set_title('Anthropomorphism')
    ax.legend()
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)
    autolabel(rects4, ax)
    autolabel(rects5, ax)

    fig.tight_layout()
    plt.show()

def getAnimacy(data):
    deadAlive = data["deadAlive"].mean()
    stagnantLively = data["stagnantLively"].mean()
    mechanicalOrganic = data["mechanicalOrganic"].mean()
    inertInteractive = data["inertInteractive"].mean()
    apatheticResponsive = data["apatheticResponsive"].mean()

    return [deadAlive, stagnantLively, mechanicalOrganic, inertInteractive, apatheticResponsive],\
           [data["deadAlive"].std(), data["stagnantLively"].std(), data["mechanicalOrganic"].std(), data["inertInteractive"].std(), data["apatheticResponsive"].std()]

def animacyBarChart(data, data_std, labels):
    length = len(data)
    x_labels = labels

    # Set plot parameters
    fig, ax = plt.subplots()
    width = 0.1  # width of bar
    x = np.arange(length)

    print(x)
    print(data[:, 0])
    rects1 = ax.bar(x, data[:, 0], width, color='green', label='Dead Alive', yerr=data_std[:, 0])
    rects2 = ax.bar(x + width, data[:, 1], width, color='#0F52BA', label='Stagnant Lively', yerr=data_std[:, 1])
    rects3 = ax.bar(x + (2 * width), data[:, 2], width, color='#6593F5', label='Mechanical Organic', yerr=data_std[:, 2])
    rects4 = ax.bar(x + (3 * width), data[:, 3], width, color='#73C2FB', label='Inert Interactive', yerr=data_std[:, 3])
    rects5 = ax.bar(x + (4 * width), data[:, 4], width, color='red', label='Apathetic Responsive', yerr=data_std[:, 4])

    ax.set_ylabel('Likert Item Value')
    ax.set_ylim(0, 6)
    ax.set_xticks(x + width + width / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Conditions')
    ax.set_title('Animacy')
    ax.legend()
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)
    autolabel(rects4, ax)
    autolabel(rects5, ax)

    fig.tight_layout()
    plt.show()

def getLikeability(data):
    dislikeLike = data["dislikeLike"].mean()
    unfriendlyFriendly = data["unfriendlyFriendly"].mean()
    unkindKind = data["unkindKind"].mean()
    unpleasantPleasant = data["unpleasantPleasant"].mean()
    awfulNice = data["awfulNice"].mean()

    return [dislikeLike, unfriendlyFriendly, unkindKind, unpleasantPleasant, awfulNice],\
           [data["dislikeLike"].std(), data["unfriendlyFriendly"].std(), data["unkindKind"].std(), data["unpleasantPleasant"].std(), data["awfulNice"].std()]

def likeabilityBarChart(data, data_std, labels):
    length = len(data)
    x_labels = labels

    # Set plot parameters
    fig, ax = plt.subplots()
    width = 0.1  # width of bar
    x = np.arange(length)

    print(x)
    print(data[:, 0])
    rects1 = ax.bar(x, data[:, 0], width, color='green', label='Dislike Like', yerr=data_std[:, 0])
    rects2 = ax.bar(x + width, data[:, 1], width, color='#0F52BA', label='Unfriendly Friendly', yerr=data_std[:, 1])
    rects3 = ax.bar(x + (2 * width), data[:, 2], width, color='#6593F5', label='Unkind Kind', yerr=data_std[:, 2])
    rects4 = ax.bar(x + (3 * width), data[:, 3], width, color='#73C2FB', label='Unpleasant Pleasant', yerr=data_std[:, 3])
    rects5 = ax.bar(x + (4 * width), data[:, 4], width, color='red', label='Awful Nice', yerr=data_std[:, 4])

    ax.set_ylabel('Likert Item Value')
    ax.set_ylim(0, 6)
    ax.set_xticks(x + width + width / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Conditions')
    ax.set_title('Likeability')
    ax.legend()
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)
    autolabel(rects4, ax)
    autolabel(rects5, ax)

    fig.tight_layout()
    plt.show()

def getPerceivedIntelligence(data):
    incompetentCompetent = data["incompetentCompetent"].mean()
    ignorantKnowledgeable = data["ignorantKnowledgeable"].mean()
    irresponsibleResponsible = data["irresponsibleResponsible"].mean()
    unintelligentIntelligent = data["unintelligentIntelligent"].mean()
    foolishSensible = data["foolishSensible"].mean()

    return [incompetentCompetent, ignorantKnowledgeable, irresponsibleResponsible, unintelligentIntelligent, foolishSensible],\
           [data["incompetentCompetent"].std(), data["ignorantKnowledgeable"].std(), data["irresponsibleResponsible"].std(), data["unintelligentIntelligent"].std(), data["foolishSensible"].std()]

def perceivedIntelligenceBarChart(data, data_std, labels):
    length = len(data)
    x_labels = labels

    # Set plot parameters
    fig, ax = plt.subplots()
    width = 0.1  # width of bar
    x = np.arange(length)

    print(x)
    print(data[:, 0])
    rects1 = ax.bar(x, data[:, 0], width, color='green', label='Incompetent Competent', yerr=data_std[:, 0])
    rects2 = ax.bar(x + width, data[:, 1], width, color='#0F52BA', label='Ignorant Knowledgeable', yerr=data_std[:, 1])
    rects3 = ax.bar(x + (2 * width), data[:, 2], width, color='#6593F5', label='Irresponsible Responsible', yerr=data_std[:, 2])
    rects4 = ax.bar(x + (3 * width), data[:, 3], width, color='#73C2FB', label='Unintelligent Intelligent', yerr=data_std[:, 3])
    rects5 = ax.bar(x + (4 * width), data[:, 4], width, color='red', label='Foolish Sensible', yerr=data_std[:, 4])

    ax.set_ylabel('Likert Item Value')
    ax.set_ylim(0, 6)
    ax.set_xticks(x + width + width / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Conditions')
    ax.set_title('Perceived Intelligence')
    ax.legend()
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)
    autolabel(rects4, ax)
    autolabel(rects5, ax)

    fig.tight_layout()
    plt.show()

def replaceItemInList(toReplace, substitute, data):
    return [substitute if x == toReplace else x for x in data]

def educationHistogram(data, title="Education Levels of Participants"):
    education = data["education"].tolist()
    education = replaceItemInList(0, "None", education)
    education = replaceItemInList(9, "GED/Secondary", education)
    education = replaceItemInList(2, "High School", education)
    education = replaceItemInList(3, "Technical", education)
    education = replaceItemInList(4, "Bachelors", education)
    education = replaceItemInList(5, "Masters", education)
    education = replaceItemInList(6, "Doctorate", education)
    print(education)
    plotHistogram(education, 7)
    plt.title(title)
    plt.show()


def relationshipHistogram(data, title="Type of Relationship"):
    relationship = data["typeOfRelationship"].tolist()
    relationship = replaceItemInList(1, "Sibling", relationship)
    relationship = replaceItemInList(2, "Classmate/Colleague", relationship)
    relationship = replaceItemInList(3, "Stranger", relationship)
    relationship = replaceItemInList(4, "Relative", relationship)
    relationship = replaceItemInList(5, "Friend", relationship)
    relationship = replaceItemInList(6, "Parent", relationship)
    relationship = replaceItemInList(7, "Teacher/Coach", relationship)
    relationship = replaceItemInList(8, "Neighbour", relationship)
    print(relationship)
    plotHistogram(relationship, 8)
    plt.title(title)
    plt.show()

def motivationDifferences(data):
    prior = data["motivationBefore"].tolist()
    during = data["motivation"].tolist()
    post = data["motivationAfter"].tolist()
    diffPD = []
    diffDA = []
    for i in range(0, len(prior)):
        diffPD.append(during[i] - prior[i])
        diffDA.append(post[i] - during[i])

    return [mean(diffPD), mean(diffDA)], [stdev(diffPD), stdev(diffDA)]

def motivationDifferencesBarChart(data, data_std, labels):
    length = len(data)
    x_labels = labels

    # Set plot parameters
    fig, ax = plt.subplots()
    width = 0.1  # width of bar
    x = np.arange(length)

    print(x)
    print(data[:, 0])
    rects1 = ax.bar(x, data[:, 0], width, color='green', label='Before to During Change', yerr=data_std[:, 0])
    rects2 = ax.bar(x + width, data[:, 1], width, color='#0F52BA', label='During to After Change', yerr=data_std[:, 1])

    ax.set_ylabel('Average Change in motivation')
    ax.set_ylim(-1.5, 2)
    ax.set_xticks(x + width + width / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Conditions')
    ax.set_title('Change in Motivation')
    ax.legend()
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    autolabel(rects1, ax)
    autolabel(rects2, ax)

    fig.tight_layout()
    plt.show()

def safetyDifferences(data):
    anxiousBefore = data["anxiousRelaxedBefore"].tolist()
    agitatedCalmBefore = data["agitatedCalmBefore"].tolist()
    quiescentSurprisedBefore = data["quiescentSurprisedBefore"].tolist()
    anxiousAfter = data["anxiousRelaxedAfter"].tolist()
    agitatedCalmAfter = data["agitatedCalmAfter"].tolist()
    quiescentSurprisedAfter = data["quiescentSurprisedAfter"].tolist()
    diffAnxious = []
    diffCalm = []
    diffSurprised = []
    for i in range(0, len(anxiousBefore)):
        diffAnxious.append(anxiousAfter[i] - anxiousBefore[i])
        diffCalm.append(agitatedCalmAfter[i] - agitatedCalmBefore[i])
        diffSurprised.append(quiescentSurprisedAfter[i] - quiescentSurprisedBefore[i])

    return [mean(diffAnxious), mean(diffCalm), mean(diffSurprised)], [stdev(diffAnxious), stdev(diffCalm), stdev(diffSurprised)]

def safetyDifferencesBarChart(data, data_std, labels):
    length = len(data)
    x_labels = labels

    # Set plot parameters
    fig, ax = plt.subplots()
    width = 0.1  # width of bar
    x = np.arange(length)

    print(x)
    print(data[:, 0])
    rects1 = ax.bar(x, data[:, 0], width, color='green', label='Anxious/Relaxed', yerr=data_std[:, 0])
    rects2 = ax.bar(x + width, data[:, 1], width, color='#0F52BA', label='Agitated/Calm', yerr=data_std[:, 1])
    rects3 = ax.bar(x + (2 * width), data[:, 2], width, color='#6593F5', label='Quiescent/Surprised', yerr=data_std[:, 2])

    ax.set_ylabel('Average Change in motivation')
    ax.set_ylim(-2, 2)
    ax.set_xticks(x + width + width / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Conditions')
    ax.set_title('Change in Safety')
    ax.legend()
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)

    fig.tight_layout()
    plt.show()

def dietDiabetes(data):
    usefulOrNotDiabetes = data["usefulOrNotDiabetes"].tolist()
    usefulOrNotObesity = data["usefulOrNotObesity"].tolist()
    convenience = data["convenience"].tolist()
    preference = data["preference"].tolist()
    understandingDiabetes = data["understandingDiabetes"].tolist()

    return [mean(usefulOrNotDiabetes), mean(usefulOrNotObesity), mean(convenience), mean(preference), mean(understandingDiabetes)], [stdev(usefulOrNotDiabetes), stdev(usefulOrNotObesity), stdev(convenience), stdev(preference), stdev(understandingDiabetes)]

def dietDiabetesBarChart(data, data_std, labels):
    length = len(data)
    x_labels = labels

    # Set plot parameters
    fig, ax = plt.subplots()
    width = 0.1  # width of bar
    x = np.arange(length)

    print(x)
    print(data[:, 0])
    rects1 = ax.bar(x, data[:, 0], width, color='green', label='Useful Or Not Diabetes', yerr=data_std[:, 0])
    rects2 = ax.bar(x + width, data[:, 1], width, color='#0F52BA', label='Useful Or Not Obesity', yerr=data_std[:, 1])
    rects3 = ax.bar(x + (2 * width), data[:, 2], width, color='#6593F5', label='Convenience', yerr=data_std[:, 2])
    rects4 = ax.bar(x + (3 * width), data[:, 3], width, color='#73C2FB', label='Preference', yerr=data_std[:, 3])
    rects5 = ax.bar(x + (4 * width), data[:, 4], width, color='red', label='Understanding Diabetes', yerr=data_std[:, 4])

    ax.set_ylabel('Likert Item Value')
    ax.set_ylim(0, 6)
    ax.set_xticks(x + width + width / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Conditions')
    ax.set_title('Diet, Diabetes, Preferences')
    ax.legend()
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)
    autolabel(rects4, ax)
    autolabel(rects5, ax)

    fig.tight_layout()
    plt.show()

data = pd.read_csv("output_files/summary.csv")
data1 = pd.read_csv("output_files/summary_1.csv")
data2 = pd.read_csv("output_files/summary_2.csv")
data3 = pd.read_csv("output_files/summary_3.csv")
'''
#Efficacy
efficacyHistogram(data)
efficacyHistogram(data1)
efficacyHistogram(data2)
efficacyHistogram(data3)
#Efficacy Difference
efficacyDifference(data)
efficacyDifference(data1)
efficacyDifference(data2)
efficacyDifference(data3)
'''
#Demographics

#Age
ageHistogram(data)
#Gender
genderHistogram(data)

#Anthropomorphism
all, allError = getAnthropomorphism(data)
first, firstError = getAnthropomorphism(data1)
second, secondError = getAnthropomorphism(data2)
third, thirdError = getAnthropomorphism(data3)

anthropomorphismBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

all, allError = getAnimacy(data)
first, firstError = getAnimacy(data1)
second, secondError = getAnimacy(data2)
third, thirdError = getAnimacy(data3)

animacyBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

all, allError = getLikeability(data)
first, firstError = getLikeability(data1)
second, secondError = getLikeability(data2)
third, thirdError = getLikeability(data3)

likeabilityBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

all, allError = getPerceivedIntelligence(data)
first, firstError = getPerceivedIntelligence(data1)
second, secondError = getPerceivedIntelligence(data2)
third, thirdError = getPerceivedIntelligence(data3)

perceivedIntelligenceBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

relationshipHistogram(data)
educationHistogram(data)

all, allError = motivationDifferences(data)
first, firstError = motivationDifferences(data1)
second, secondError = motivationDifferences(data2)
third, thirdError = motivationDifferences(data3)

motivationDifferencesBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

all, allError = safetyDifferences(data)
first, firstError = safetyDifferences(data1)
second, secondError = safetyDifferences(data2)
third, thirdError = safetyDifferences(data3)

safetyDifferencesBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

all, allError = dietDiabetes(data)
first, firstError = dietDiabetes(data1)
second, secondError = dietDiabetes(data2)
third, thirdError = dietDiabetes(data3)

dietDiabetesBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

