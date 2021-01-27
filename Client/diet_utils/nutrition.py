class Nutrition:
    def __init__(self, age, weight, height, gender):
        self.age = age
        self.weight = weight
        self.height = height
        self.heightMeters = self.height/100
        self.gender = gender
        self.BMI = self.weight / (self.heightMeters * self.heightMeters)

    def TotalEnergyExpenditure(self):
        if self.gender is "male":
            return (66 + (13.7 * self.weight) + (5 * self.height) - (6.8 * self.age)) * (0.5)
        else:
            return (655 + (9.6 * self.weight) + (1.8 * self.height) - (4.7 * self.age)) * (0.5)

    def BodyMassIndex(self):
        return self.weight/(self.heightMeters*self.heightMeters)

    #Based off of the 2015 Dietary Guidelines for Americans Advisory Group where no more than 10% of daily caloric intake should be from sugar.
    def SugarIntake(self):
        tee = self.TotalEnergyExpenditure()
        print(tee)
        self.recommendedMaxSugarIntake = 0.1 * tee
        self.recommendedMinSugarIntake = 0.06 * tee

    def SugarGramsToCalories(self, gramsSugar):
        return 4 * gramsSugar

    def AppropriateGoals(self, calorieIntake=0, sugarIntake=0):
        self.SugarIntake()
        if calorieIntake is 0:
            calorieIntake = self.TotalEnergyExpenditure()
        if sugarIntake is 0:
            sugarIntake = self.recommendedMaxSugarIntake

        CI = True
        SI = True
        #People need at least 1200 calories or 60% of daily expenditure.
        if calorieIntake < 0.7 * self.TotalEnergyExpenditure():
            print("Calorie Intake not Appropriate")
            CI = False

        if sugarIntake < 0.5 * self.recommendedMinSugarIntake:
            print("Sugar Intake not Appropriate")
            SI = False

        return CI, SI

    def AppropriateGoalsBMI(self):
        CI = True
        SI = True
        classification = self.BMIClassification(self.BMI)
        if classification < 2:
            CI = False

        return CI, SI

    def BMIClassification(self, BMI):
        #Underweight
        if BMI < 18.5:
            return 0
        #Normal
        if BMI < 25:
            return 1
        #Overweight
        if BMI < 30:
            return 2
        #Obese
        return 3
