import pandas as pd
import spacy

class DietLikes:
    def __init__(self):
        df = pd.read_csv('../resources/NutritionFacts.csv')

        df = df[df["Food Group"] != "Baby Foods"]
        df = df[df["Food Group"] != "Spices and Herbs"]
        df = df[df["Food Group"] != "Fats and Oils"]
        df = df[df['Food Group'].notna()]

        self.conversations = df["Name"].tolist()
        self.nlp = spacy.load('en_core_web_md')
        self.calories = df["Calories"].tolist()
        self.sugar = df["Sugars (g)"].tolist()
        self.foodgroups = df["Food Group"].tolist()

    def getLikeStatement(self, like, goal=0):
        #Use tf-idf to find all items with similar descriptions
        #print(conversations)

        similarities = []
        questionDoc = self.nlp(like)

        for item in range(len(self.conversations)):
            conversation = self.conversations[item]
            questDoc = self.nlp(conversation)
            sim = questDoc.similarity(questionDoc)
            similarities.append(sim)

        top7 = sorted(range(len(similarities)), key=lambda i: similarities[i])[-7:]
        top7Items = []
        for i in top7:
            top7Items.append([self.conversations[i], self.calories[i], self.sugar[i], self.foodgroups[i]])

        maxItem = 0
        maximum = -1
        minimum = -1
        minItem = 0

        type = 1
        if goal is 0:
            type = 1
        else:
            type = 2

        for i in range(0, len(top7Items)):
            if top7Items[i][type] > maximum:
                maximum = top7Items[i][type]
                maxItem = i
            if minimum is -1 or top7Items[i][type] < minimum:
                minimum = top7Items[i][type]
                minItem = i

        print(top7Items[maxItem])
        print(top7Items[minItem])

        statement = "While you could have something like " + str(top7Items[maxItem][0]) + ", something like " + str(top7Items[minItem][0]) + " may be a healthier choice "
        if goal is 0:
            statement = statement + "due to the lower amount of calories if it is available to you."
        else:
            statement = statement + "due to the lower amount of sugar if it is available to you."
        return statement