from statistics import mean, stdev, mode, median

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

np.set_printoptions(precision=4)

def plotHistogram(valueList, binsNum, label="None", range=None):
    plt.hist(valueList, bins=binsNum, alpha=0.5, range=range, label=label, edgecolor='black')

def efficacyHistogram(data, title="User Efficacy"):
    plotHistogram(data["priorEfficacy"].tolist(), 5, "Prior")
    plotHistogram(data["postEfficacy"].tolist(), 5, "Post")
    plt.legend(loc='upper right')
    plt.title(title)
    plt.show()
    print("Efficacy")
    print(data["priorEfficacy"].median())
    print("Prior Efficacy", data["priorEfficacy"].mean(), data["priorEfficacy"].std())
    print(data["postEfficacy"].median())
    print("Post Efficacy", data["postEfficacy"].mean(), data["postEfficacy"].std())

def efficacyDifference(data, title="User Efficacy Difference"):
    prior = data["priorEfficacy"].tolist()
    post = data["postEfficacy"].tolist()
    diff = []
    for i in range(0, len(prior)):
        diff.append(post[i] - prior[i])
    print("Efficacy Difference")
    plotHistogram(diff, 5)
    plt.title(title)
    plt.show()
    print(median(diff))
    print("Efficacy Difference", np.mean(diff), np.std(diff))

def genderHistogram(data, title="Participants by Gender"):
    genders = data["gender"].tolist()

    plotHistogram(genders, 3)
    plt.title(title)
    plt.show()

def ageHistogram(data, title="Participants by Age"):
    age = data["age"].tolist()

    plotHistogram(age, 8, range=[18, 60])
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

    print("Antropomorphism")
    print(data["fakeNatural"].median(), data["machineHuman"].median(), data["consciousUnconscious"].median(), data["artificialLifelike"].median(), data["rigidElegant"].median())
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
    ax.set_ylim(0, 5)
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

    print("Animacy")
    print(data["deadAlive"].median(), data["stagnantLively"].median(), data["mechanicalOrganic"].median(),
          data["inertInteractive"].median(), data["apatheticResponsive"].median())
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

    print("Likeability")
    print(data["dislikeLike"].median(), data["unfriendlyFriendly"].median(), data["unkindKind"].median(),
          data["unpleasantPleasant"].median(), data["awfulNice"].median())
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

    print("Perceived Intelligence")
    print(data["incompetentCompetent"].median(), data["ignorantKnowledgeable"].median(), data["irresponsibleResponsible"].median(),
          data["unintelligentIntelligent"].median(), data["foolishSensible"].median())
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
    plotHistogram(education, 6)
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

    print("Motivation")
    print(median(post), median(during))
    return [mean(post), mean(during)], [stdev(post), stdev(during)], diffPD, diffDA

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
    diffAnxious = anxiousAfter
    diffCalm = agitatedCalmAfter
    diffSurprised = quiescentSurprisedAfter

    '''
    for i in range(0, len(anxiousBefore)):
        diffAnxious.append(anxiousAfter[i] - anxiousBefore[i])
        diffCalm.append(agitatedCalmAfter[i] - agitatedCalmBefore[i])
        diffSurprised.append(quiescentSurprisedAfter[i] - quiescentSurprisedBefore[i])
    '''

    print("Safety Differences")
    print(median(diffAnxious), median(diffCalm),
          median(diffSurprised))
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

    print("Diet Diabetes")
    print(median(usefulOrNotDiabetes), median(usefulOrNotObesity),
          median(convenience), median(preference), median(understandingDiabetes))
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

def boxPlot(data, labels, title):
    fig, ax = plt.subplots()
    ax.boxplot(data)
    ax.set_xticklabels(labels)

    plt.title(title)

    plt.show()

def claimsQuestions(data):
    engagement = data["engagement"].tolist()
    autonomy = data["autonomy"].tolist()
    negativePositive = data["positiveNegative"].tolist()

    print("Claims")
    print(median(engagement), median(autonomy),
          median(negativePositive))
    return [mean(engagement), mean(autonomy), mean(negativePositive)], [stdev(engagement), stdev(autonomy), stdev(negativePositive)]

def claimsBarChart(data, data_std, labels):
    length = len(data)
    x_labels = labels

    # Set plot parameters
    fig, ax = plt.subplots()
    width = 0.1  # width of bar
    x = np.arange(length)

    print(x)
    print(data[:, 0])
    rects1 = ax.bar(x, data[:, 0], width, color='green', label='Engagement', yerr=data_std[:, 0])
    rects2 = ax.bar(x + width, data[:, 1], width, color='#0F52BA', label='Autonomy', yerr=data_std[:, 1])
    rects3 = ax.bar(x + (2 * width), data[:, 2], width, color='#6593F5', label='Negative/Positive Experience', yerr=data_std[:, 2])

    ax.set_ylabel('Likert Item Value')
    ax.set_ylim(0, 6)
    ax.set_xticks(x + width + width / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Conditions')
    ax.set_title('Claims Questions')
    ax.legend()
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)

    fig.tight_layout()
    plt.show()

def Categories(data):
    anthropomorphism = data["anthropomorphism"].tolist()
    animacy = data["animacy"].tolist()
    likeability = data["likeability"].tolist()
    intelligence = data["perceivedIntelligence"].tolist()
    safetyBefore = data["safetyBefore"].tolist()
    safetyAfter = data["safetyAfter"].tolist()
    safetyChange = data["safetyChange"].tolist()

    print("Categories")
    print(median(anthropomorphism), median(animacy),
          median(likeability), median(intelligence), median(safetyBefore), median(safetyAfter), median(safetyChange))
    return [mean(anthropomorphism), mean(animacy), mean(likeability), mean(intelligence), mean(safetyBefore), mean(safetyAfter), mean(safetyChange)],\
           [stdev(anthropomorphism), stdev(animacy), stdev(likeability), stdev(intelligence), stdev(safetyBefore), stdev(safetyAfter), stdev(safetyChange)]

def categoriesBarChart(data, data_std, labels):
    length = len(data)
    x_labels = labels

    # Set plot parameters
    fig, ax = plt.subplots()
    width = 0.1  # width of bar
    x = np.arange(length)

    print(x)
    print(data[:, 0])
    rects1 = ax.bar(x, data[:, 0], width, color='green', label='Anthropomorphism', yerr=data_std[:, 0])
    rects2 = ax.bar(x + width, data[:, 1], width, color='#0F52BA', label='Animacy', yerr=data_std[:, 1])
    rects3 = ax.bar(x + (2 * width), data[:, 2], width, color='#6593F5', label='Likeability', yerr=data_std[:, 2])
    rects4 = ax.bar(x + (3 * width), data[:, 3], width, color='red', label='Perceived Intelligence', yerr=data_std[:, 3])
    rects5 = ax.bar(x + (4 * width), data[:, 4], width, color='green', label='Safety Before', yerr=data_std[:, 4])
    rects6 = ax.bar(x + (5 * width), data[:, 5], width, color='brown', label='Safety After', yerr=data_std[:, 5])
    rects7 = ax.bar(x + (6 * width), data[:, 6], width, color='purple', label='Safety Change', yerr=data_std[:, 6])



    ax.set_ylabel('Likert Item Value')
    ax.set_ylim(0, 27)
    ax.set_xticks(x + width + width / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Conditions')
    ax.set_title('Categorical Values')
    ax.legend()
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)
    autolabel(rects4, ax)
    autolabel(rects5, ax)
    autolabel(rects6, ax)
    autolabel(rects7, ax)

    fig.tight_layout()
    plt.show()

data = pd.read_csv("output_files/summary.csv")
data1 = pd.read_csv("output_files/summary_1.csv")
data2 = pd.read_csv("output_files/summary_2.csv")
data3 = pd.read_csv("output_files/summary_3.csv")

#Efficacy
#efficacyHistogram(data)
#efficacyHistogram(data1)
#efficacyHistogram(data2)
#efficacyHistogram(data3)
#Efficacy Difference
#efficacyDifference(data)
#efficacyDifference(data1)
#efficacyDifference(data2)
#efficacyDifference(data3)

#Demographics

#Age
#ageHistogram(data)
#educationHistogram(data)

'''
#Anthropomorphism
all, allError = getAnthropomorphism(data)
print(all, allError)
first, firstError = getAnthropomorphism(data1)
print(first, firstError)
second, secondError = getAnthropomorphism(data2)
print(second, secondError)
third, thirdError = getAnthropomorphism(data3)
print(third, thirdError)

anthropomorphismBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

all, allError = getAnimacy(data)
print(all, allError)
first, firstError = getAnimacy(data1)
print(first, firstError)
second, secondError = getAnimacy(data2)
print(second, secondError)
third, thirdError = getAnimacy(data3)
print(third, thirdError)

animacyBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

all, allError = getLikeability(data)
print(all, allError)
first, firstError = getLikeability(data1)
print(first, firstError)
second, secondError = getLikeability(data2)
print(second, secondError)
third, thirdError = getLikeability(data3)
print(third, thirdError)

likeabilityBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])


all, allError = getPerceivedIntelligence(data)
print(all, allError)
first, firstError = getPerceivedIntelligence(data1)
print(first, firstError)
second, secondError = getPerceivedIntelligence(data2)
print(second, secondError)
third, thirdError = getPerceivedIntelligence(data3)
print(third, thirdError)

perceivedIntelligenceBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

relationshipHistogram(data)
educationHistogram(data)


all, allError = safetyDifferences(data)
print(all, allError)
first, firstError = safetyDifferences(data1)
print(first, firstError)
second, secondError = safetyDifferences(data2)
print(second, secondError)
third, thirdError = safetyDifferences(data3)
print(third, thirdError)

safetyDifferencesBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

all, allError = dietDiabetes(data)
print(all, allError)
first, firstError = dietDiabetes(data1)
print(first, firstError)
second, secondError = dietDiabetes(data2)
print(second, secondError)
third, thirdError = dietDiabetes(data3)
print(third, thirdError)

dietDiabetesBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])


all, allError = claimsQuestions(data)
print(all, allError)
first, firstError = claimsQuestions(data1)
print(first, firstError)
second, secondError = claimsQuestions(data2)
print(second, secondError)
third, thirdError = claimsQuestions(data3)
print(third, thirdError)

claimsBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

#Gender
genderHistogram(data)

_, _, all, allError = motivationDifferences(data)
_, _, first, firstError = motivationDifferences(data1)
_, _, second, secondError = motivationDifferences(data2)
_, _, third, thirdError = motivationDifferences(data3)

print(mode(first), mode(second), third)
boxPlot([all, first, second, third], ["All", "First", "Second", "Third"], "Comparison of Motivation Change")

all, allError, _, _ = motivationDifferences(data)
print(all, allError)
first, firstError, _, _ = motivationDifferences(data1)
print(first, firstError)
second, secondError, _, _ = motivationDifferences(data2)
print(second, secondError)
third, thirdError, _, _ = motivationDifferences(data3)
print(third, thirdError)

motivationDifferencesBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])

relationshipHistogram(data)
'''
'''
items = [data, data1, data2, data3]

for item in items:
    print("ITEM")
    words = item["futureWork"].tolist()

    #print(mean(words), stdev(words), median(words))
    print(Counter(words).keys()) # equals to list(set(words))
    print(Counter(words).values()) # counts the elements' frequency
'''

all, allError, = Categories(data)
print(all, allError)
first, firstError, = Categories(data1)
print(first, firstError)
second, secondError, = Categories(data2)
print(second, secondError)
third, thirdError, = Categories(data3)
print(third, thirdError)

categoriesBarChart(np.array([all, first, second, third]), np.array([allError, firstError, secondError, thirdError]), ["All", "1", "2", "3"])
