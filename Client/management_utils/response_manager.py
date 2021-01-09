import re

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
        yes = ["yes", "okay", "yep", "yah",]
        no = ["no", "nope", "nah", "don't", "not", "nay", "now"]
        decision = 0
        if self.MatchExpectedResponses(yes, Response):
            decision = 1
        elif self.MatchExpectedResponses(no, Response):
            decision = 0
        else:
            decision = 2

        return decision

    #Returns a 0,1,or 2. 0 is femalel. 1 is a male. 2 is neither.
    def DetermineGender(self, Response):
        male = ["male", "man", "boy", "masculine",]
        female = ["female", "woman", "girl", "feminine"]
        decision = 0
        if self.MatchExpectedResponses(male, Response):
            decision = 1
        elif self.MatchExpectedResponses(female, Response):
            decision = 0
        else:
            decision = 2

        return decision

    def GetNumber(self, Response):
        numbers = [int(word) for word in Response.split() if word.isdigit()]
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