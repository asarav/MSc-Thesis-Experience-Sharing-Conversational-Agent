from nltk import tokenize
from operator import itemgetter
import math
from nltk.corpus import stopwords
from rake_nltk import Rake
stop_words = set(stopwords.words('english'))
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

#Simple example to determine how to parse statements for rephrasing as a shared experience.
question = "How do you think you will feel when you achieve your goal?"

doc = "I think I will feel a sense of pride if I manage to reach my goal."

class ExperienceManager:
    def __init__(self, question, doc):
        self.question = question
        self.doc = doc

    def TFIDFKeywordExtraction(self, question, doc):
        total_words = doc.split()
        total_word_length = len(total_words)
        print(total_word_length)

        total_sentences = tokenize.sent_tokenize(doc)
        total_sent_len = len(total_sentences)
        print(total_sent_len)

        tf_score = {}
        for each_word in total_words:
            each_word = each_word.replace('.', '')
            if each_word not in stop_words:
                if each_word in tf_score:
                    tf_score[each_word] += 1
                else:
                    tf_score[each_word] = 1

        # Dividing by total_word_length for each dictionary element
        tf_score.update((x, y / int(total_word_length)) for x, y in tf_score.items())
        print(tf_score)

        def check_sent(word, sentences):
            final = [all([w in x for w in word]) for x in sentences]
            sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
            return int(len(sent_len))

        idf_score = {}
        for each_word in total_words:
            each_word = each_word.replace('.', '')
            if each_word not in stop_words:
                if each_word in idf_score:
                    idf_score[each_word] = check_sent(each_word, total_sentences)
                else:
                    idf_score[each_word] = 1

        # Performing a log and divide
        idf_score.update((x, math.log(int(total_sent_len) / y)) for x, y in idf_score.items())

        print(idf_score)

        tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
        print(tf_idf_score)

        def get_top_n(dict_elem, n):
            result = dict(sorted(dict_elem.items(), key=itemgetter(1), reverse=True)[:n])
            return result

        print(get_top_n(tf_idf_score, 5))

    def RakeKeywordExtraction(self, question, doc):
        r = Rake()  # Uses stopwords for english from NLTK, and all puntuation characters.

        r.extract_keywords_from_text(doc)

        rankedPhrases = r.get_ranked_phrases()  # To get keyword phrases ranked highest to lowest.
        print(rankedPhrases)

    def NLTKPOSTagging(self, document):
        sent = nltk.word_tokenize(document)
        sent = nltk.pos_tag(sent)
        return sent

    def SPACYPOSTagging(self, document):
        answer = nlp(document)
        print(answer)
        for token in answer:
            return token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop