import pickle
from os import path

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report

class QuestionDetector:
    def __init__(self):
        if path.exists("./models/vectorizer.pk") and path.exists("./models/gradientBooster.pk"):
            print("exists")
            v = open("./models/vectorizer.pk", 'rb')
            g = open("./models/gradientBooster.pk", 'rb')
            self.vectorizer = pickle.load(v)
            self.gb = pickle.load(g)
        else:
            nltk.download('nps_chat')
            posts = nltk.corpus.nps_chat.xml_posts()


            posts_text = [post.text for post in posts]

            #divide train and test in 80 20
            train_text = posts_text[:int(len(posts_text)*0.8)]
            test_text = posts_text[int(len(posts_text)*0.2):]

            #Get TFIDF features
            self.vectorizer = TfidfVectorizer(ngram_range=(1,3),
                                         min_df=0.001,
                                         max_df=0.7,
                                         analyzer='word')

            X_train = self.vectorizer.fit_transform(train_text)
            X_test = self.vectorizer.transform(test_text)

            with open('../models/vectorizer.pk', 'wb') as fin:
                pickle.dump(self.vectorizer, fin)

            y = [post.get('class') for post in posts]

            y_train = y[:int(len(posts_text)*0.8)]
            y_test = y[int(len(posts_text)*0.2):]

            # Fitting Gradient Boosting classifier to the Training set
            self.gb = GradientBoostingClassifier(n_estimators = 400, random_state=0)

            #Can be improved with Cross Validation
            self.gb.fit(X_train, y_train)
            with open('../models/gradientBooster.pk', 'wb') as fin:
                pickle.dump(self.gb, fin)

            predictions_rf = self.gb.predict(X_test)

            #Accuracy of 86% not bad
            print(classification_report(y_test, predictions_rf))

    def Predictions(self, sentence):
        return self.gb.predict(self.vectorizer.transform([sentence]))

    def IsQuestion(self, sentence):
        prediction = self.gb.predict(self.vectorizer.transform([sentence]))
        if len(prediction) > 0:
            answer = prediction[0]
            if "whQuestion" == answer:
                return True
            elif "ynQuestion" == answer:
                return True
            else:
                return False
        else:
            return False