from os import listdir
from os.path import isfile, join

from data_retrieval.dietItemManager import DietLikes
from data_retrieval.jsonManager import jsonManager
from experience_management.experienceManager import ExperienceManager
import language_tool_python

from experience_management.sentimentDetection import performSentimentAnalysis
tool = language_tool_python.LanguageTool('en-US')

def rewordPhrase(answer):
    rewordedPraise = answer
    rewordedPraise = rewordedPraise.replace("I'm", "you were")
    rewordedPraise = rewordedPraise.replace("I am", "you were")
    rewordedPraise = rewordedPraise.replace("I", "You")
    rewordedPraise = rewordedPraise.replace(" me ", " you ")
    rewordedPraise = rewordedPraise.replace(" me.", "you.")
    rewordedPraise = rewordedPraise.replace(" my ", " your ")
    rewordedPraise = rewordedPraise.replace("My ", "Your ")
    rewordedPraise = rewordedPraise.replace(" my.", " your.")
    rewordedPraise = rewordedPraise.replace(" mine ", " yours ")
    rewordedPraise = rewordedPraise.replace(" mine.", " yours.")
    rewordedPraise = rewordedPraise.replace(" myself.", " yourself.")
    rewordedPraise = rewordedPraise.replace(" myself ", " yourself ")
    return rewordedPraise

#Look through all memory files
mypath = "../interaction_data"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)

for file in onlyfiles:
    print(file)
    if file == "session.json":
        continue
    manager = jsonManager()
    manager.readJSON(mypath + "/" + file)
    fileData = manager.data
    dietLikeManager = DietLikes()
    if "session" in fileData:
        if (fileData["session"] is 2) or (fileData["session"] is 3):
            #Add diet advice
            if "dietLikes" in fileData and fileData["session"] is 2:
                dietLike = fileData["dietLikes"]
                goal = fileData["goal"]
                answer = dietLikeManager.getLikeStatement(dietLike["question"], goal)
                fileData["dietLikes"]["answer"] = answer
            if "experiences" in fileData:
                experiences = fileData["experiences"]
                currentSession = fileData["session"]
                updatedExperiences = []
                # For each memory file, iterate through the individual experiences
                for experience in experiences:
                    # Use spellcheck and generate variations of the sentence to handle any problems with speech recognition.
                    print(experience)
                    question = experience["Question"]
                    answer = experience["Answer"]

                    praisePhrases = []
                    criticismPhrases = []

                    #Do some filtering of words like "oh", "yeah", and other words like "God" and the names of others
                    stopwords = ['oh', 'yeah', 'God', 'Charlie', 'god']
                    querywords = answer.split()

                    resultwords = [word for word in querywords if word.lower() not in stopwords]
                    filteredAnswer = ' '.join(resultwords)

                    memoryUpdater = ExperienceManager(question, filteredAnswer)
                    #Use rake for keyword extraction, because it is better
                    print("RAKE")
                    keywords = memoryUpdater.RakeKeywordExtraction()
                    print(keywords)

                    #Use spellcheck to get a replacement that can be used as the basis of a rephrased memory.
                    print("Matches")
                    correctedAnswer = tool.correct(answer)
                    answer = correctedAnswer

                    #Remove keywords that do not contain nouns or adjectives
                    # Use NLTK for POS tagging, because it is easier to work with
                    if len(keywords) > 0:
                        parts = memoryUpdater.NLTKPOSTaggingSpecific(keywords[0])
                        print("POS")
                        print(parts)
                        for part in parts:
                            if part[1] == 'JJ' or part[1] == "JJR" or part[1] == 'NN' or part[1] == 'NNS':
                                print("Good")

                    #For each memory, perform sentiment analysis and keyword extraction for the question and the answer
                    sentiment = performSentimentAnalysis(answer)
                    print(sentiment)
                    sentimentBool = False
                    if sentiment == "Positive":
                        sentimentBool = True

                    # SESSION 1 MEMORIES



                    #Determine context of experience (just using hardcoded questions)
                    #Generate sentences that can be used for reuse.
                    #First generate variants for praise
                    if question == "Are you feeling excited to start? Nervous? What feelings are you having right now?":
                        if currentSession is 2:
                            #Keyword
                            keywordPraise = ""
                            if len(keywords) > 0:
                                keywordPraise = "In our first session, I asked you how you were feeling before we started. "
                                keywordPraise = keywordPraise + "You mentioned " + keywords[0] + "."
                                keywordPraise = keywordPraise + " Honestly, I think you have nothing to worry about and that it's fine to be more excited, because you are doing great!"

                                print("KeywordPraise")
                                print(keywordPraise)
                                praisePhrases.append(keywordPraise)

                            #Rewording with sentiment (rewording only does not allow for deeper meaning to be interpretted)
                            rewordedPraise = rewordPhrase(filteredAnswer)
                            rewordedPraise = "In our first session, you said " + rewordedPraise + " when asked about how you were feeling before starting."
                            if sentimentBool:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded positive, and I hope you maintain that level of positivity in your future efforts."
                            else:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded a bit negative, but as you can see, you have nothing to worry about. You are doing a great job."

                            print("Reworded Praise")
                            print(rewordedPraise)
                            praisePhrases.append(rewordedPraise)

                            #Praise with only sentiment
                            sentimentPraise = ""
                            if sentimentBool:
                                sentimentPraise = "In our first session, I asked you how you were feeling before you got started, and you sounded optimistic and positive. Keep it up. Your optimism will help you in the long run."
                            else:
                                sentimentPraise = "In our first session, I asked you how you were feeling before you got started, and you sounded a bit pessimistic, but I think it's fine to be a bit more optimistic. You have done well, and I'm sure you will continue to do well."
                            praisePhrases.append(sentimentPraise)

                            #Second generate variants for criticism
                            #Keyword
                            keywordCriticism = ""
                            if len(keywords) > 0:
                                keywordCriticism = "In our first session, I asked you how you were feeling before we started. "
                                keywordCriticism = keywordCriticism + "You mentioned " + keywords[0] + "."
                                keywordCriticism = keywordCriticism + " Honestly, I think you don't need to worry and doing so would be counterproductive. I think what would help would be to stay optimistic and focus on consistent activity. Stay focused, and I'm sure you will make it."
                                criticismPhrases.append(keywordCriticism)

                            #Rewording with sentiment
                            rewordedCriticism = rewordPhrase(filteredAnswer)
                            rewordedCriticism = "In our first session, you said " + rewordedCriticism + " when asked about how you were feeling before starting."
                            if sentimentBool:
                                rewordedCriticism = rewordedCriticism + " When you said that, you sounded positive, and I hope you maintain that level of positivity in your future efforts despite the shortcomings you have had in meeting your goal."
                            else:
                                rewordedCriticism = rewordedCriticism + " When you said that, you sounded a bit negative, and this may be hurting you in your efforts to reach your goal. Stay motivated, positive and focused, and I'm sure you will reach your goal."
                            criticismPhrases.append(rewordedCriticism)

                            #Praise with only sentiment
                            sentimentCriticism = ""
                            if sentimentBool:
                                sentimentCriticism = "In our first session, I asked you how you were feeling before you got started, and you sounded optimistic and positive. Even though you've run into some problems, I don't think this should change. Stay consistent and committed. You will get there."
                            else:
                                sentimentCriticism = "In our first session, I asked you how you were feeling before you got started, and you sounded a bit pessimistic, but I think it's fine to be a bit more optimistic. The fact that you are here shows that you want to work towards your goal. You just need to take the first step."
                            criticismPhrases.append(sentimentCriticism)
                        else:
                            # Keyword
                            keywordPraise = ""
                            if len(keywords) > 0:
                                keywordPraise = "In our first session, I asked you how you were feeling before we started. "
                                keywordPraise = keywordPraise + "You mentioned " + keywords[0] + "."
                                keywordPraise = keywordPraise + " Given your ability to meet your milestone, there was nothing to worry about."

                                print("KeywordPraise")
                                print(keywordPraise)
                                praisePhrases.append(keywordPraise)

                            # Rewording with sentiment (rewording only does not allow for deeper meaning to be interpretted)
                            rewordedPraise = rewordPhrase(filteredAnswer)
                            rewordedPraise = "In our first session, you said " + rewordedPraise + " when asked about how you were feeling before starting."
                            if sentimentBool:
                                rewordedPraise = rewordedPraise + " You sounded quite optimistic, and I am sure that led you to reach your milestone in the second session."
                            else:
                                rewordedPraise = rewordedPraise + " You sounded a bit negative, but it seems that it did not affect you at all, because you managed to reach your milestone in the second session."

                            print("Reworded Praise")
                            print(rewordedPraise)
                            praisePhrases.append(rewordedPraise)

                            # Praise with only sentiment
                            sentimentPraise = ""
                            if sentimentBool:
                                sentimentPraise = "In our first session, I asked you how you were feeling before you got started, and you sounded optimistic and positive. It looks like this helped you to reach your milestone."
                            else:
                                sentimentPraise = "In our first session, I asked you how you were feeling before you got started, and you sounded a bit pessimistic, but it looks like this did not hold you back at all, because you managed to reach your final milestone."
                            praisePhrases.append(sentimentPraise)

                            # Second generate variants for criticism
                            # Keyword
                            keywordCriticism = ""
                            if len(keywords) > 0:
                                keywordCriticism = "In our first session, I asked you how you were feeling before we started. "
                                keywordCriticism = keywordCriticism + "You mentioned " + keywords[0] + "."
                                keywordCriticism = keywordCriticism + " It seems that you may have been a bit nervous or worried, because you did not manage to reach your milestone. A more optimistic and focused outlook may have served you better."
                                criticismPhrases.append(keywordCriticism)

                            # Rewording with sentiment
                            rewordedCriticism = rewordPhrase(filteredAnswer)
                            rewordedCriticism = "In our first session, you said " + rewordedCriticism + " when asked about how you were feeling before starting."
                            if sentimentBool:
                                rewordedCriticism = rewordedCriticism + " You sounded a bit positive, and despite your shortcoming and inability to meet your milestone, I hope you stayed positive and focused on your goal."
                            else:
                                rewordedCriticism = rewordedCriticism + " You sounded a bit negative, and that might have hurt your ability to meet your milestone. A more positive and focused outlook may have worked to your benefit."
                            criticismPhrases.append(rewordedCriticism)

                            # Praise with only sentiment
                            sentimentCriticism = ""
                            if sentimentBool:
                                sentimentCriticism = "In our first session, I asked you how you were feeling before you got started, and you sounded optimistic and positive. Even though you did not meet your milestone, I hope this did not change. Staying consistent and committed will surely help you in the long run."
                            else:
                                sentimentCriticism = "In our first session, I asked you how you were feeling before you got started, and you sounded a bit pessimistic, but I think if you were a bit more optimistic, you would have had more success. The fact that you are here and you want to work towards your goal already means you are making some progress."
                            criticismPhrases.append(sentimentCriticism)




                    elif question == "Why would you like to work on this goal?":
                        if currentSession is 2:
                            goal = fileData["goal"]
                            # Keyword
                            keywordPraise = ""
                            if len(keywords) > 0:
                                keywordPraise = "In our first session, I asked you why you would like to work on "
                                if goal is 0:
                                    keywordPraise = keywordPraise + "calorie restriction."
                                else:
                                    keywordPraise = keywordPraise + "sugar reduction."
                                keywordPraise = keywordPraise + " You mentioned " + keywords[0] + "."
                                keywordPraise = keywordPraise + " It looks like you had that in the back of your head as you were working towards your goal, because the results so far are very promising. Keep it up."

                                print("KeywordPraise")
                                print(keywordPraise)
                                praisePhrases.append(keywordPraise)

                            # Rewording with sentiment (rewording only does not allow for deeper meaning to be interpretted)
                            rewordedPraise = rewordPhrase(filteredAnswer)
                            rewordedPraise = "In our first session, you said " + rewordedPraise + " when asked about why you would like to work on "
                            if goal is 0:
                                rewordedPraise = rewordedPraise + "calorie restriction."
                            else:
                                rewordedPraise = rewordedPraise + "sugar reduction."
                            if sentimentBool:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded positive, and I hope you maintain that level of positivity in your future efforts."
                            else:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded a bit negative, but as you can see, you have nothing to worry about. You are doing a great job."

                            print("Reworded Praise")
                            print(rewordedPraise)
                            praisePhrases.append(rewordedPraise)

                            # Praise with only sentiment
                            sentimentPraise = "In our first session, I asked you why you wanted to work on "
                            if goal is 0:
                                sentimentPraise = sentimentPraise + "calorie restriction"
                            else:
                                sentimentPraise = sentimentPraise + "sugar reduction"
                            if sentimentBool:
                                sentimentPraise = sentimentPraise + ", and you sounded optimistic and positive. Keep it up. Your optimism will help you in the long run."
                            else:
                                sentimentPraise = sentimentPraise + ", and you sounded a bit pessimistic, but I think it's fine to be a bit more optimistic. You have done well, and I'm sure you will continue to do well."
                            praisePhrases.append(sentimentPraise)

                            # Second generate variants for criticism
                            # Keyword
                            keywordCriticism = ""
                            if len(keywords) > 0:
                                keywordCriticism = "In our first session, I asked you why you would like to work on "
                                if goal is 0:
                                    keywordCriticism = keywordCriticism + "calorie restriction."
                                else:
                                    keywordCriticism = keywordCriticism + "sugar reduction."
                                keywordCriticism = keywordCriticism + " You mentioned " + keywords[0] + "."
                                keywordCriticism = keywordCriticism + " You had some setbacks, but I think if you keep these thoughts in mind and focus, you will reach your goal."
                                criticismPhrases.append(keywordCriticism)

                            # Rewording with sentiment
                            rewordedCriticism = rewordPhrase(filteredAnswer)
                            rewordedCriticism = "In our first session, you said " + rewordedCriticism + " when I asked you why you would like to work on "
                            if goal is 0:
                                rewordedCriticism = rewordedCriticism + "calorie restriction."
                            else:
                                rewordedCriticism = rewordedCriticism + "sugar reduction."
                            if sentimentBool:
                                rewordedCriticism = rewordedCriticism + " When you said that, you sounded positive, and I hope you maintain that level of positivity in your future efforts despite the shortcomings you have had in meeting your goal."
                            else:
                                rewordedCriticism = rewordedCriticism + " When you said that, you sounded a bit negative, and this may be hurting you in your efforts to reach your goal. Stay motivated, positive and focused, and I'm sure you will reach your goal."
                            criticismPhrases.append(rewordedCriticism)

                            # Praise with only sentiment
                            sentimentCriticism = "In our first session, I asked you why you wanted to work on "
                            if goal is 0:
                                sentimentCriticism = sentimentCriticism + "calorie restriction"
                            else:
                                sentimentCriticism = sentimentCriticism + "sugar reduction"
                            if sentimentBool:
                                sentimentCriticism = sentimentCriticism + ", and you sounded optimistic and positive. Even though you've run into some problems, I don't think this should change. Stay consistent and committed. You will get there."
                            else:
                                sentimentCriticism = sentimentCriticism + ", and you sounded a bit pessimistic, but I think it's fine to be a bit more optimistic. The fact that you are here shows that you want to work towards your goal. You just need to take the first step."
                            criticismPhrases.append(sentimentCriticism)
                        else:
                            goal = fileData["goal"]
                            # Keyword
                            keywordPraise = ""
                            if len(keywords) > 0:
                                keywordPraise = "In our first session, I asked you why you would like to work on "
                                if goal is 0:
                                    keywordPraise = keywordPraise + "calorie restriction."
                                else:
                                    keywordPraise = keywordPraise + "sugar reduction."
                                keywordPraise = keywordPraise + " You mentioned " + keywords[0] + "."
                                keywordPraise = keywordPraise + " It looks like you had that in the back of your head as you were working towards your goal, because you managed to reach your milestone, and I hope it helped you when you were working towards your final goal as well."

                                print("KeywordPraise")
                                print(keywordPraise)
                                praisePhrases.append(keywordPraise)

                            # Rewording with sentiment (rewording only does not allow for deeper meaning to be interpretted)
                            rewordedPraise = rewordPhrase(filteredAnswer)
                            rewordedPraise = "In our first session, you said " + rewordedPraise + " when asked about why you would like to work on "
                            if goal is 0:
                                rewordedPraise = rewordedPraise + "calorie restriction."
                            else:
                                rewordedPraise = rewordedPraise + "sugar reduction."
                            if sentimentBool:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded positive. I am sure this helped you reach your milestone and I hope you used that positivity in your journey towards your final goal as well."
                            else:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded a bit negative, but it seems that there was no need to be negative, because you managed to reach your milestone. I hope you were able to improve on your milestone in your approach towards your final goal."

                            print("Reworded Praise")
                            print(rewordedPraise)
                            praisePhrases.append(rewordedPraise)

                            # Praise with only sentiment
                            sentimentPraise = "In our first session, I asked you why you wanted to work on "
                            if goal is 0:
                                sentimentPraise = sentimentPraise + "calorie restriction"
                            else:
                                sentimentPraise = sentimentPraise + "sugar reduction"
                            if sentimentBool:
                                sentimentPraise = sentimentPraise + ", and you sounded optimistic and positive. I'm sure that helped you in your milestone, and I hope it helped you with your final goal."
                            else:
                                sentimentPraise = sentimentPraise + ", and you sounded a bit pessimistic, but I think it's fine to be a bit more optimistic. You managed to reach your milestone, and I'm sure that a more optimistic outlook will help you in other endeavors as well."
                            praisePhrases.append(sentimentPraise)

                            # Second generate variants for criticism
                            # Keyword
                            keywordCriticism = ""
                            if len(keywords) > 0:
                                keywordCriticism = "In our first session, I asked you why you would like to work on "
                                if goal is 0:
                                    keywordCriticism = keywordCriticism + "calorie restriction."
                                else:
                                    keywordCriticism = keywordCriticism + "sugar reduction."
                                keywordCriticism = keywordCriticism + " You mentioned " + keywords[0] + "."
                                keywordCriticism = keywordCriticism + " You may not have met your milestone, but I think if you keep these thoughts in mind and focus, it will help you in future endeavors."
                                criticismPhrases.append(keywordCriticism)

                            # Rewording with sentiment
                            rewordedCriticism = rewordPhrase(filteredAnswer)
                            rewordedCriticism = "In our first session, you said " + rewordedCriticism + " when I asked you why you would like to work on "
                            if goal is 0:
                                rewordedCriticism = rewordedCriticism + "calorie restriction."
                            else:
                                rewordedCriticism = rewordedCriticism + "sugar reduction."
                            if sentimentBool:
                                rewordedCriticism = rewordedCriticism + " When you said that, you sounded positive, and I hope you managed to maintain that level of positivity in your efforts towards your final goal despite the shortcomings you have had in meeting your milestone."
                            else:
                                rewordedCriticism = rewordedCriticism + " When you said that, you sounded a bit negative, and this may have hurt you in your efforts to reach your milestone. I hope you managed to stay motivated, positive and focused in your efforts to reach your final goal."
                            criticismPhrases.append(rewordedCriticism)

                            # Praise with only sentiment
                            sentimentCriticism = "In our first session, I asked you why you wanted to work on "
                            if goal is 0:
                                sentimentCriticism = sentimentCriticism + "calorie restriction"
                            else:
                                sentimentCriticism = sentimentCriticism + "sugar reduction"
                            if sentimentBool:
                                sentimentCriticism = sentimentCriticism + ", and you sounded optimistic and positive. Even though you did not meet your milestone, I don't think this should change and I hope you stayed consistent and committed in your efforts towards your final goal."
                            else:
                                sentimentCriticism = sentimentCriticism + ", and you sounded a bit pessimistic, but I think it's fine to be a bit more optimistic. You you may not have met your first milestone, but I'm sure that optimism would have helped you with your final goal."
                            criticismPhrases.append(sentimentCriticism)





                    elif question == "If you manage to achieve this goal, how do you think you will feel?":
                        if currentSession is 2:
                            # Keyword
                            keywordPraise = ""
                            if len(keywords) > 0:
                                keywordPraise = "In our first session, I asked you how you would feel if you managed to achieve your goal. "
                                keywordPraise = keywordPraise + "You mentioned " + keywords[0] + "."
                                keywordPraise = keywordPraise + " It looks like you had that in the back of your head as you were working towards your goal, because the results so far are very promising. Keep it up and those feelings will become reality."

                                print("KeywordPraise")
                                print(keywordPraise)
                                praisePhrases.append(keywordPraise)

                            # Rewording with sentiment (rewording only does not allow for deeper meaning to be interpretted)
                            rewordedPraise = rewordPhrase(filteredAnswer)
                            rewordedPraise = "In our first session, you said " + rewordedPraise + " when asked how you would feel if you managed to achieve your goal."
                            if sentimentBool:
                                rewordedPraise = rewordedPraise +  " When you said that, you sounded positive, and I hope you maintain that level of positivity in your future efforts. Keep it up and those feelings will become reality."
                            else:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded a bit negative, but as you can see, you have nothing to worry about. You are doing a great job."

                            print("Reworded Praise")
                            print(rewordedPraise)
                            praisePhrases.append(rewordedPraise)

                            # Praise with only sentiment
                            sentimentPraise = ""
                            if sentimentBool:
                                sentimentPraise = "In our first session, I asked you how you would feel when you accomplished your goal, and you sounded optimistic and positive. Keep it up. Your optimism will help you in the long run and those feelings will become reality."
                            else:
                                sentimentPraise = "In our first session, I asked you how you would feel when you accomplished your goal, and you sounded a bit pessimistic, but I think it's fine to be a bit more optimistic. You have done well, and I'm sure you will continue to do well. I believe your goal is worth it and you are worth it."
                            praisePhrases.append(sentimentPraise)

                            # Second generate variants for criticism
                            # Keyword
                            keywordCriticism = ""
                            if len(keywords) > 0:
                                keywordCriticism = "In our first session, I asked you how you would feel when you accomplished your goal. "
                                keywordCriticism = keywordCriticism + "You mentioned " + keywords[0] + "."
                                keywordCriticism = keywordCriticism + " If you want to experience those feelings and make them a reality, you will need to take the first step. I know you have it in you."
                                criticismPhrases.append(keywordCriticism)

                            # Rewording with sentiment
                            rewordedCriticism = rewordPhrase(filteredAnswer)
                            rewordedCriticism = "In our first session, you said " + rewordedCriticism + " when I asked you how you would feel when you accomplished your goal."
                            if sentimentBool:
                                rewordedCriticism = rewordedCriticism + " When you said that, you sounded positive, and I hope you maintain that level of positivity in your future efforts despite the shortcomings you have had in meeting your goal. I believe that you will one day make those feelings a reality."
                            else:
                                rewordedCriticism = rewordedCriticism + " When you said that, you sounded a bit negative, and this may be hurting you in your efforts to reach your goal. Stay motivated, positive and focused, and I'm sure you will reach your goal and make those feelings a reality."
                            criticismPhrases.append(rewordedCriticism)

                            # Praise with only sentiment
                            sentimentCriticism = ""
                            if sentimentBool:
                                sentimentCriticism = "In our first session, I asked you how you would feel when you accomplished your goal, and you sounded optimistic and positive. Even though you've run into some problems, I don't think this should change. Stay consistent and committed and those feelings will become a reality."
                            else:
                                sentimentCriticism = "In our first session, I asked you how you would feel when you accomplished you goal, and you sounded a bit pessimistic, but I think it's fine to be a bit more optimistic. The fact that you are here shows that you want to work towards your goal. You just need to take the first step and before you know it, those feelings will be reality."
                            criticismPhrases.append(sentimentCriticism)
                        else:
                            keywordPraise = ""
                            if len(keywords) > 0:
                                keywordPraise = "In our first session, I asked you how you would feel if you managed to achieve your goal. "
                                keywordPraise = keywordPraise + "You mentioned " + keywords[0] + "."
                                keywordPraise = keywordPraise + " It looks like that was in your mind as you were working towards your milestone, and I hope it helped you in your efforts towards your final goal."

                                print("KeywordPraise")
                                print(keywordPraise)
                                praisePhrases.append(keywordPraise)

                            # Rewording with sentiment (rewording only does not allow for deeper meaning to be interpretted)
                            rewordedPraise = rewordPhrase(filteredAnswer)
                            rewordedPraise = "In our first session, you said " + rewordedPraise + " when asked how you would feel if you managed to achieve your goal."
                            if sentimentBool:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded positive, and I hope you maintained that level of positivity when working towards your final goal as well."
                            else:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded a bit negative, but as you can see, you managed to meet your milestone. I hope you were able to gain a more optimistic mindset and apply it in your efforts towards your final goal."

                            print("Reworded Praise")
                            print(rewordedPraise)
                            praisePhrases.append(rewordedPraise)

                            # Praise with only sentiment
                            sentimentPraise = ""
                            if sentimentBool:
                                sentimentPraise = "In our first session, I asked you how you would feel when you accomplished your goal, and I hope you maintained that level of positivity when working towards your final goal as well."
                            else:
                                sentimentPraise = "In our first session, I asked you how you would feel when you accomplished your goal, and you sounded a bit pessimistic, but as you can see, you managed to meet your milestone. I hope you were able to gain a more optimistic mindset and apply it in your efforts towards your final goal."
                            praisePhrases.append(sentimentPraise)

                            # Second generate variants for criticism
                            # Keyword
                            keywordCriticism = ""
                            if len(keywords) > 0:
                                keywordCriticism = "In our first session, I asked you how you would feel when you accomplished your goal. "
                                keywordCriticism = keywordCriticism + "You mentioned " + keywords[0] + "."
                                keywordCriticism = keywordCriticism + " Although you did not meet your milestone, I hope you kept those feelings in mind when you were working towards your final goal. Making a positive change in your diet is definitely worth it."
                                criticismPhrases.append(keywordCriticism)

                            # Rewording with sentiment
                            rewordedCriticism = rewordPhrase(filteredAnswer)
                            rewordedCriticism = "In our first session, you said " + rewordedCriticism + " when I asked you how you would feel when you accomplished your goal."
                            rewordedCriticism = rewordedCriticism + " Although you did not meet your milestone, I hope you kept those feelings in mind when you were working towards your final goal. Making a positive change in your diet is definitely worth it."
                            criticismPhrases.append(rewordedCriticism)



                    elif question == "What will achieving this goal allow you to do that you could not do before?":
                        if currentSession is 2:
                            # Keyword
                            keywordPraise = ""
                            if len(keywords) > 0:
                                keywordPraise = "In our first session, I asked you what achieving your goal would allow you to do. "
                                keywordPraise = keywordPraise + "You mentioned " + keywords[0] + "."
                                keywordPraise = keywordPraise + " It looks like you had that in the back of your head as you were working towards your goal, because the results so far are very promising. Keep it up and you will surely be able to do those things one day."

                                print("KeywordPraise")
                                print(keywordPraise)
                                praisePhrases.append(keywordPraise)

                            # Rewording with sentiment (rewording only does not allow for deeper meaning to be interpretted)
                            rewordedPraise = rewordPhrase(filteredAnswer)
                            rewordedPraise = "In our first session, you said " + rewordedPraise + " when asked what achieving your goal would allow you to do."
                            if sentimentBool:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded positive, and I hope you maintain that level of positivity in your future efforts. Keep it up and one day you will be able to do those things."
                            else:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded a bit negative, but as you can see, you have nothing to worry about. You are doing a great job."

                            print("Reworded Praise")
                            print(rewordedPraise)
                            praisePhrases.append(rewordedPraise)

                            # Praise with only sentiment
                            sentimentPraise = ""
                            if sentimentBool:
                                sentimentPraise = "In our first session, I asked you what achieving your goal would allow you to do, and you sounded optimistic and positive. Keep it up. Your optimism will help you in the long run and one day you will be able to do those things."
                            else:
                                sentimentPraise = "In our first session, I asked you what achieving your goal would allow you to do, and you sounded a bit pessimistic, but I think it's fine to be a bit more optimistic. You have done well, and I'm sure you will continue to do well. I believe your goal is worth it and you are worth it."
                            praisePhrases.append(sentimentPraise)

                            # Second generate variants for criticism
                            # Keyword
                            keywordCriticism = ""
                            if len(keywords) > 0:
                                keywordCriticism = "In our first session, I asked you how you would feel when you accomplished your goal. "
                                keywordCriticism = keywordCriticism + "You mentioned " + keywords[0] + "."
                                keywordCriticism = keywordCriticism + " If you want to experience those feelings and make them a reality, you will need to take the first step. I know you have it in you."
                                criticismPhrases.append(keywordCriticism)

                            # Rewording with sentiment
                            rewordedCriticism = rewordPhrase(filteredAnswer)
                            rewordedCriticism = "In our first session, you said " + rewordedCriticism + " when I asked you how you would feel when you accomplished your goal."
                            if sentimentBool:
                                rewordedCriticism = rewordedCriticism + " When you said that, you sounded positive, and I hope you maintain that level of positivity in your future efforts despite the shortcomings you have had in meeting your goal. I believe that you will one day make those feelings a reality."
                            else:
                                rewordedCriticism = rewordedCriticism + " When you said that, you sounded a bit negative, and this may be hurting you in your efforts to reach your goal. Stay motivated, positive and focused, and I'm sure you will reach your goal and make those feelings a reality."
                            criticismPhrases.append(rewordedCriticism)

                            # Praise with only sentiment
                            sentimentCriticism = ""
                            if sentimentBool:
                                sentimentCriticism = "In our first session, I asked you how you would feel when you accomplished your goal, and you sounded optimistic and positive. Even though you've run into some problems, I don't think this should change. Stay consistent and committed and those feelings will become a reality."
                            else:
                                sentimentCriticism = "In our first session, I asked you how you would feel when you accomplished you goal, and you sounded a bit pessimistic, but I think it's fine to be a bit more optimistic. The fact that you are here shows that you want to work towards your goal. You just need to take the first step and before you know it, you will be able to do those things."
                            criticismPhrases.append(sentimentCriticism)
                        else:
                            # Keyword
                            keywordPraise = ""
                            if len(keywords) > 0:
                                keywordPraise = "In our first session, I asked you what achieving your goal would allow you to do. "
                                keywordPraise = keywordPraise + "You mentioned " + keywords[0] + "."
                                keywordPraise = keywordPraise + " It looks like you had that in the back of your head as you were working towards your milestone, and I hope you kept it in mind as you worked towards your final goal."

                                print("KeywordPraise")
                                print(keywordPraise)
                                praisePhrases.append(keywordPraise)

                            # Rewording with sentiment (rewording only does not allow for deeper meaning to be interpretted)
                            rewordedPraise = rewordPhrase(filteredAnswer)
                            rewordedPraise = "In our first session, you said " + rewordedPraise + " when asked what achieving your goal would allow you to do."
                            if sentimentBool:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded positive, and I hope you managed to maintain that level of positivity in your efforts towards your final goal. It did help you reach your milestone after all."
                            else:
                                rewordedPraise = rewordedPraise + " When you said that, you sounded a bit negative, but as you can see you managed to do a great job with your milestone and staying negative can hold you back. Imagine the possibilities with a more positive outlook."

                            print("Reworded Praise")
                            print(rewordedPraise)
                            praisePhrases.append(rewordedPraise)

                            # Praise with only sentiment
                            sentimentPraise = ""
                            if sentimentBool:
                                sentimentPraise = "In our first session, I asked you what achieving your goal would allow you to do, and you sounded optimistic and positive. That is good, and it definitely helped with your milestone. Your optimism will help you in the long run and I hope that it helped you with your final goal."
                            else:
                                sentimentPraise = "In our first session, I asked you what achieving your goal would allow you to do, and you sounded a bit pessimistic, but I think it was fine to be a bit more optimistic. You have done well on your milestone, and being more optimistic would have set you up for success not only for your final goal, but for any other goals you might set for yourself in the future."
                            praisePhrases.append(sentimentPraise)

                            # Second generate variants for criticism
                            # Keyword
                            keywordCriticism = ""
                            if len(keywords) > 0:
                                keywordCriticism = "In our first session, I asked you how you would feel when you accomplished your goal. "
                                keywordCriticism = keywordCriticism + "You mentioned " + keywords[0] + "."
                                keywordCriticism = keywordCriticism + " Although you did not reach your milestone, those feelings were valid. I hope you kept those feelings in mind as you worked towards your second goal."
                                criticismPhrases.append(keywordCriticism)

                            # Rewording with sentiment
                            rewordedCriticism = rewordPhrase(filteredAnswer)
                            rewordedCriticism = "In our first session, you said " + rewordedCriticism + " when I asked you how you would feel when you accomplished your goal."
                            if sentimentBool:
                                rewordedCriticism = rewordedCriticism + " When you said that, you sounded positive, and I hope you maintained that level of positivity in your efforts towards your final goal despite the shortcomings you have had in meeting your milestone. I believe that those feelings are valid and worth remembering."
                            else:
                                rewordedCriticism = rewordedCriticism + " When you said that, you sounded a bit negative. This may have not hurt you in your milestone, but and this could have hurt you in your efforts to reach your goal. Stay motivated, positive and focused, and I'm sure feelings will be easier to achieve."
                            criticismPhrases.append(rewordedCriticism)

                            # Praise with only sentiment
                            sentimentCriticism = ""
                            if sentimentBool:
                                sentimentCriticism = "In our first session, I asked you how you would feel when you accomplished your goal, and you sounded optimistic and positive. Even though you did not meet your milestone, I don't think this should change. If you wanted to see those feelings will become a reality, I believe and hope that you maintained that mindset."
                            else:
                                sentimentCriticism = "In our first session, I asked you how you would feel when you accomplished you goal, and you sounded a bit pessimistic. This may have hurt you when you were working towards your milestone, and I think it's fine to be a bit more optimistic. The fact that you are here shows that you want to work towards your goal, so you've already made some progress."
                            criticismPhrases.append(sentimentCriticism)



                    # SESSION 2 MEMORIES
                    elif question == "Now that you have started, how do you feel about the progress you have made?":
                        # Keyword
                        keywordPraise = ""
                        if len(keywords) > 0:
                            keywordPraise = "In our second session, I asked you how you felt about the progress you made. "
                            keywordPraise = keywordPraise + "You mentioned " + keywords[0] + "."
                            if sentimentBool:
                                keywordPraise = keywordPraise + " It sounded like things were looking up for you, and I imagine that helped you reach your final goal."
                            else:
                                keywordPraise = keywordPraise + " It sounded like things were not looking up for you, which was unfortunate, but you managed to push through and reach your goal."
                            keywordPraise = keywordPraise + " Overall, looking back on things and how you managed to meet your final goal, I think it's time to start celebrating."

                            print("KeywordPraise")
                            print(keywordPraise)
                            praisePhrases.append(keywordPraise)

                        # Rewording with sentiment (rewording only does not allow for deeper meaning to be interpretted)
                        rewordedPraise = rewordPhrase(filteredAnswer)
                        rewordedPraise = "In our second session, you said " + rewordedPraise + " when asked how you felt about the progress you made so far."
                        if sentimentBool:
                            rewordedPraise = rewordedPraise + " It sounded like things were looking up for you, and I imagine that helped you reach your final goal."
                        else:
                            rewordedPraise = rewordedPraise + " It sounded like things were not looking up for you, which was unfortunate, but you managed to push through and reach your goal."
                        rewordedPraise = rewordedPraise + " Overall, looking back on things and how you managed to meet your final goal, I think it's time to start celebrating."

                        print("Reworded Praise")
                        print(rewordedPraise)
                        praisePhrases.append(rewordedPraise)

                        # Second generate variants for criticism
                        # Keyword
                        keywordCriticism = ""
                        if len(keywords) > 0:
                            keywordCriticism = "In our second session, I asked you how you felt about the progress you made. "
                            keywordCriticism = keywordCriticism + "You mentioned " + keywords[0] + "."
                            if sentimentBool:
                                keywordCriticism = keywordCriticism + " It sounded like things were looking up for you, which is a bit unfortunate, but it looks like you made some progress regardless of whether you met your goal or not."
                            else:
                                keywordCriticism = keywordCriticism + " It sounded like things were not looking up for you, which is a bit unfortunate, but hopefully you at least now know what is involved in working towards a goal, and what habits to follow."
                            criticismPhrases.append(keywordCriticism)

                        # Rewording with sentiment
                        rewordedCriticism = rewordPhrase(filteredAnswer)
                        rewordedCriticism = "In our second session, you said " + rewordedCriticism + " when asked how you felt about the progress you made so far."
                        if sentimentBool:
                            rewordedCriticism = rewordedCriticism + " It sounded like things were looking up for you, which is a bit unfortunate, but it looks like you made some progress regardless of whether you met your goal or not."
                        else:
                            rewordedCriticism = rewordedCriticism + " It sounded like things were not looking up for you, which is a bit unfortunate, but hopefully you at least now know what is involved in working towards a goal, and what habits to follow."
                        criticismPhrases.append(rewordedCriticism)




                    elif question == "What are you struggling with?":
                        # Keyword
                        keywordPraise = ""
                        if len(keywords) > 0:
                            keywordPraise = "In our second session, I asked what you were struggling with. "
                            keywordPraise = keywordPraise + "You mentioned " + keywords[0] + "."
                            keywordPraise = keywordPraise + " It sounds like you managed to at least partially address some of these struggles, because you did well in meeting your final goal."

                            print("KeywordPraise")
                            print(keywordPraise)
                            praisePhrases.append(keywordPraise)

                        # Rewording with sentiment (rewording only does not allow for deeper meaning to be interpretted)
                        rewordedPraise = rewordPhrase(filteredAnswer)
                        rewordedPraise = "In our second session, you said " + rewordedPraise + " when asked how you felt about the progress you made so far."
                        if sentimentBool:
                            rewordedPraise = rewordedPraise + " It sounded like the struggles that you had were not that difficult to solve to begin with, and you managed to overcome them to ."
                        else:
                            rewordedPraise = rewordedPraise + " It sounded like those struggles were quite challenging, but you managed to get past them, so great job!"

                        print("Reworded Praise")
                        print(rewordedPraise)
                        praisePhrases.append(rewordedPraise)

                        # Second generate variants for criticism
                        # Keyword
                        keywordCriticism = ""
                        if len(keywords) > 0:
                            keywordCriticism = "In our second session, I asked what you were struggling with. "
                            keywordCriticism = keywordCriticism + "You mentioned " + keywords[0] + "."
                            keywordCriticism = keywordCriticism + " It sounded like those things may have still been a problem in your efforts towards your final goal. Although you did not reach your final goal, I hope you at least gained some experience by going through this process and learned a bit about diet along the way."
                            criticismPhrases.append(keywordCriticism)

                        # Rewording with sentiment
                        rewordedCriticism = rewordPhrase(filteredAnswer)
                        rewordedCriticism = "In our second session, you said " + rewordedCriticism + " when asked how you felt about the progress you made so far."
                        rewordedCriticism = rewordedCriticism + " It sounded like those things may have still been a problem in your efforts towards your final goal. Although you did not reach your final goal, I hope you at least gained some experience by going through this process and learned a bit about diet along the way."
                        criticismPhrases.append(rewordedCriticism)




                    elif question == "How do you think your family, friends or coworkers would react if they heard about you reaching your goal?":
                        # Keyword
                        keywordPraise = ""
                        if len(keywords) > 0:
                            keywordPraise = "In our second session, I asked you how you think your family, friends or coworkers would react if they heard about you reaching your goal. "
                            keywordPraise = keywordPraise + "You mentioned " + keywords[0] + "."

                            if sentimentBool:
                                keywordPraise = keywordPraise + " Well, you've reached your goal, so I imagine you will be able to see their reactions soon, and I hope that you are looking forward to a positive response."
                            else:
                                keywordPraise = keywordPraise + " You did not sound too optimistic, but you should realize that you have managed to accomplish a lot, and people will recognize that effort. Great job."

                            print("KeywordPraise")
                            print(keywordPraise)
                            praisePhrases.append(keywordPraise)

                        # Rewording with sentiment (rewording only does not allow for deeper meaning to be interpretted)
                        rewordedPraise = rewordPhrase(filteredAnswer)
                        rewordedPraise = "In our second session, you said " + rewordedPraise + " when asked how you think your family, friends or coworkers would react if they heard about you reaching your goal."
                        if sentimentBool:
                            rewordedPraise = rewordedPraise + " Well, you've reached your goal, so I imagine you will be able to see their reactions soon, and I hope that you are looking forward to a positive response."
                        else:
                            rewordedPraise = rewordedPraise + " You did not sound too optimistic, but you should realize that you have managed to accomplish a lot, and people will recognize that effort. Great job."

                        print("Reworded Praise")
                        print(rewordedPraise)
                        praisePhrases.append(rewordedPraise)

                        # Second generate variants for criticism
                        # Keyword
                        keywordCriticism = ""
                        if len(keywords) > 0:
                            keywordCriticism = "In our second session, I asked you how you think your family, friends or coworkers would react if they heard about you reaching your goal. "
                            keywordCriticism = keywordCriticism + "You mentioned " + keywords[0] + "."

                            keywordCriticism = keywordCriticism + " Although you haven't reached your goal, you have made some progress just by going through this process, and I think those in your inner circle will recognize that as well."

                            criticismPhrases.append(keywordCriticism)

                        # Rewording with sentiment
                        rewordedCriticism = rewordPhrase(filteredAnswer)
                        rewordedCriticism = "In our second session, you said " + rewordedCriticism + " when I asked you how you think your family, friends or coworkers would react if they heard about you reaching your goal."
                        rewordedCriticism = rewordedCriticism + " Although you haven't reached your goal, you have made some progress just by going through this process, and I think those in your inner circle will recognize that as well."
                        criticismPhrases.append(rewordedCriticism)

                    #Add reworded phrases to data
                    newExperience = experience
                    newExperience["praise"] = praisePhrases
                    newExperience["criticism"] = criticismPhrases
                    updatedExperiences.append(newExperience)
                fileData["experiences"] = updatedExperiences
    manager.data = fileData
    #Use this as a temporary file to test
    manager.writeDataToJSON(mypath + "/" + file)
