from os import listdir
from os.path import isfile, join

from data_retrieval.jsonManager import jsonManager
from experience_management.experienceManager import ExperienceManager
import language_tool_python

from experience_management.sentimentDetection import performSentimentAnalysis

tool = language_tool_python.LanguageTool('en-US')

#Look through all memory files
mypath = "../interaction_data"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)

for file in onlyfiles:
    print(file)
    manager = jsonManager()
    manager.readJSON(mypath + "/" + file)
    fileData = manager.data
    if "session" in fileData:
        if (fileData["session"] is 2) or (fileData["session"] is 3):
            if "experiences" in fileData:
                experiences = fileData["experiences"]
                # For each memory file, iterate through the individual experiences
                for experience in experiences:
                    # Use spellcheck and generate variations of the sentence to handle any problems with speech recognition.
                    print(experience)
                    question = experience["Question"]
                    answer = experience["Answer"]

                    memoryUpdater = ExperienceManager(question, answer)
                    #Use rake for keyword extraction, because it is better
                    print("RAKE")
                    memoryUpdater.RakeKeywordExtraction()
                    #Use NLTK for POS tagging, because it is easier to work with
                    print("NLTKPOS")
                    print(memoryUpdater.NLTKPOSTagging())
                    #Use spellcheck to get a replacement that can be used as the basis of a rephrased memory.
                    print("Matches")
                    matches = tool.check(answer)
                    print(len(matches))
                    for match in matches:
                        print(match)

                    #Do some filtering of words like "oh", "yeah", and other words like "God" and the names of others

                    #For each memory, perform sentiment analysis and keyword extraction for the question and the answer
                    performSentimentAnalysis(answer)

                    #Determine context of experience (just using hardcoded questions)

                    #Generate sentences that can be used for reuse.

                    #Generate reworded sentence where "I" and "me" are replaced with "you" and mine is replaced with "your".

                    #Determine context of usages