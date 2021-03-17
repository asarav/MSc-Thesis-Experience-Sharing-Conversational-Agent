import re
from nltk import tokenize
import random
from nltk.tokenize.treebank import TreebankWordDetokenizer

class ResponseManager:
    def __init__(self):
        return

    #Checks if the response contains some form of the expected response.
    #A bit crude, because it can disregard parts that don't match and can contradict the meaning.
    def MatchExpectedResponses(self, ExpectedResponses, Response):
        for expectedResponse in ExpectedResponses:
            if expectedResponse.lower() in Response.lower():
                return True
        return False

    #Checks if one of the strings in one array is a string in the other array.
    def ContainsWord(self, ExpectedResponses, Response):
        words = self.getWords(Response)
        for word in words:
            for expectedResponse in ExpectedResponses:
                if expectedResponse.lower() in word.lower():
                    return True
        return False

    #Responses should be an array of strings with [@] to indicate variables
    #Variables should be an array of variables.
    def ResponseVariableExtractor(self, ExpectedResponses, Variables, Response):
        return

    def StringToNumber(self, Response):
        return

    #Returns the words in a string.
    #May need to handle punctuation
    def getWords(self, Response):
        words = re.sub("[^\w]", " ",  Response).split()
        return words

    #Returns a 0,1,or 2. 0 is a no. 1 is a yes. 2 is neither a yes or a no.
    def YesOrNo(self, Response):
        yes = ["yes", "okay", "yep", "yah", "yeah", "correct", "right", "agree", "agreed", "sure", "fine", "guess", "chess"]
        no = ["no", "nope", "nah", "don't", "not", "nay", "now", "doubt", "know", "incorrect", "wrong", "disagree", "disagreed"]
        decision = 0
        if self.MatchExpectedResponses(no, Response):
            decision = 0
        elif self.MatchExpectedResponses(yes, Response):
            decision = 1
        else:
            #Treat all other answers as though they are a no to prevent accidentally progressing in the flow.
            decision = 0
            #decision = 2

        return decision

    def YesOrNoSearch(self, Response):
        yes = ["yes", "okay", "yep", "yah", "yeah", "correct", "right", "agree", "agreed", "sure", "fine", "guess", "chess"]
        no = ["no", "nope", "nah", "don't", "not", "nay", "now", "doubt", "know", "incorrect", "wrong", "disagree", "disagreed"]
        decision = 0
        if self.MatchExpectedResponses(no, Response):
            decision = 0
        elif self.MatchExpectedResponses(yes, Response):
            decision = 1
        else:
            #Treat all other answers as though they are a yes to prevent accidentally progressing in the flow.
            decision = 1
            #decision = 2

        return decision

    #Returns a 0,1,or 2. 0 is femalel. 1 is a male. 2 is neither.
    def DetermineGender(self, Response):
        male = ["male", "man", "boy", "masculine", "mail"]
        female = ["female", "woman", "girl", "feminine"]
        decision = 0
        if self.MatchExpectedResponses(female, Response):
            decision = 0
        elif self.MatchExpectedResponses(male, Response):
            decision = 1
        else:
            decision = 2

        return decision

    def GetNumber(self, Response):
        Response = Response.strip('"')
        Response = Response.strip('cmkgftinlb')
        numbers = [int(word) for word in Response.split() if word.isdigit()]
        print(Response)
        print(type(Response))
        print(Response.isdigit())
        print(len(numbers))
        if len(numbers) is 0 and Response.isdigit():
            num = int(Response)
            numbers.append(num)

        print(numbers)
        return numbers

    def GetHeight(self, Response):
        # Imperial
        feet = ["foot", "feet"]
        inches = ["inch", "inches"]

        # Metric
        meters = ["meter", "meters"]
        centimeters = ["centimeter", "centimeters"]

        f = self.MatchExpectedResponses(feet, Response)
        i = self.MatchExpectedResponses(inches, Response)
        m = self.MatchExpectedResponses(meters, Response)
        c = self.MatchExpectedResponses(centimeters, Response)

        if f or i:
            print("Imperial")
        elif m or c:
            print("Metric")
        else:
            print("Unknown")

    def GetGoal(self, Response):
        calorieRestriction = ["calorie", "caloric"]
        sugarReduction = ["sugar", "glucose"]
        dietCompositionChange = ["diet", "composition"]
        decision = 0
        if self.MatchExpectedResponses(calorieRestriction, Response):
            decision = 0
        elif self.MatchExpectedResponses(sugarReduction, Response):
            decision = 1
        elif self.MatchExpectedResponses(dietCompositionChange, Response):
            decision = 2
        else:
            decision = 3

        return decision

    def AskRepeat(self, Response):
        repeatKeyWords = ["could you repeat", "can you repeat", "that repeated", "not hear", "did not hear", "could not hear", "not catch",
                          "didn't hear", "couldn't hear", "didn't catch", "couldn't catch", "was not able to hear", "wasn't able to hear",
                          "was not able to catch", "wasn't able to catch", "can't hear", "cannot hear", "can't catch", "cannot catch"]
        decision = False
        if self.MatchExpectedResponses(repeatKeyWords, Response):
            decision = True

        return decision

    def AddVoiceGestures(self, Statement):
        #Used in the sentence in the start of statement
        startGestures = ["hhmmmm", "aahhhh", "ohhhh", "ummmmm", "aahhhh", "ummmmm", "sooo", "okay", "alright"]
        #Can be used whenever
        middleGestures = ["ummmm", "ummmm", "just"]

        sentences = tokenize.sent_tokenize(Statement)
        gestureNumbers = [0, 0, 0, 0, 0, 1, 1]

        if len(sentences) > 5:
            gestureNumbers.append(2)

        gestureNumber = random.choice(gestureNumbers)
        useStartGesture = False

        if gestureNumber < 2:
            useStartGesture = bool(random.choice([0, 0, 1]))
        else:
            useStartGesture = True

        # Add start gesture if needed
        if useStartGesture:
            sentences[0] = "<prosody volume=\"soft\" rate=\"x-slow\">" + random.choice(startGestures) + "</prosody>" + " " + sentences[0]

        # Add middle gestures if needed.
        if useStartGesture:
            gestureNumber = gestureNumber - 1

        if gestureNumber > 0:
            sentencesToChooseFrom = list(range(0, len(sentences)))
            while(gestureNumber > 0):
                #Choose sentence
                sentenceIndex = random.choice(sentencesToChooseFrom)
                sentencesToChooseFrom.pop(sentenceIndex)

                sentence = sentences[sentenceIndex]

                #Split the sentence into words and add the voice gesture after the randomly chosen word.
                words = str.split(sentence)
                #If the sentence is just one word, there's not much point in using the voice gesture.
                if len(words) > 1:
                    wordIndex = random.choice(list(range(0, len(words)-1)))
                    #Get the voice gesture
                    gesture = random.choice(middleGestures)
                    words[wordIndex:wordIndex] = ["<prosody volume=\"soft\" rate=\"x-slow\">" + gesture + "</prosody>"]

                    #Update sentence in list
                    updatedSentence = " ".join(words)

                    sentences[sentenceIndex] = updatedSentence

                gestureNumber = gestureNumber - 1

        finalStatement = " ".join(sentences)
        return finalStatement

    def GetProlificId(self, Statement):
        if "my ID is" in Statement:
            id = Statement.split("my ID is", 1)[1]
        elif "my user ID is" in Statement:
            id = Statement.split("my user ID is", 1)[1]
        elif "the user ID is" in Statement:
            id = Statement.split("the user ID is", 1)[1]
        elif "the ID is" in Statement:
            id = Statement.split("the ID is", 1)[1]
        elif "it is" in Statement:
            id = Statement.split("it is", 1)[1]
        elif "hello my ID is" in Statement:
            id = Statement.split("hello my ID is", 1)[1]
        elif "hello my user ID is" in Statement:
            id = Statement.split("hello my user ID is", 1)[1]
        elif "hello the user ID is" in Statement:
            id = Statement.split("hello the user ID is", 1)[1]
        elif "hello the ID is" in Statement:
            id = Statement.split("hello the ID is", 1)[1]
        elif "hello it is" in Statement:
            id = Statement.split("hello it is", 1)[1]
        elif "hi my ID is" in Statement:
            id = Statement.split("hi my ID is", 1)[1]
        elif "hi my user ID is" in Statement:
            id = Statement.split("hi my user ID is", 1)[1]
        elif "hi the user ID is" in Statement:
            id = Statement.split("hi the user ID is", 1)[1]
        elif "hi the ID is" in Statement:
            id = Statement.split("hi the ID is", 1)[1]
        elif "hi it is" in Statement:
            id = Statement.split("hi it is", 1)[1]
        else:
            id = Statement
        id.strip()
        id = id.replace(" ", "")
        return id.upper()

    def GetName(self, Statement):
        if "my name is" in Statement:
            id = Statement.split("my name is", 1)[1]
        elif "I am" in Statement:
            id = Statement.split("I am", 1)[1]
        elif "I'm" in Statement:
            id = Statement.split("I'm", 1)[1]
        elif "i am" in Statement:
            id = Statement.split("i am", 1)[1]
        elif "I would like to be called" in Statement:
            id = Statement.split("I would like to be called", 1)[1]
        elif "i would like to be called" in Statement:
            id = Statement.split("i would like to be called", 1)[1]
        else:
            id = Statement
        id.strip()
        id = id.replace(" ", "")
        return id