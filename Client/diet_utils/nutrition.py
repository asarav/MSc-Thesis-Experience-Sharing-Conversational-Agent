class Nutrition:
    def __init__(self, age, weight, height, gender):
        self.age = age
        self.weight = weight
        self.height = height
        self.heightMeters = self.height/100
        self.gender = gender
        self.BMI = self.weight / (self.heightMeters * self.heightMeters)

    def TotalEnergyExpenditure(self):
        # Physical Activity. Assume that it is sedentary for now.
        PA = 1
        if self.gender is "male":
            return 864 - (9.72 * self.age) + (PA * ((14.2 * self.weight) + (503 * self.heightMeters)))
        else:
            return 387 - (7.31 * self.age) + (PA * ((10.9 * self.weight) + (660.7 * self.heightMeters)))

    def BodyMassIndex(self):
        return self.weight/(self.heightMeters*self.heightMeters)

    #Based off of the 2015 Dietary Guidelines for Americans Advisory Group where no more than 10% of daily caloric intake should be from sugar.
    def SugarIntake(self):
        self.recommendedMaxSugarIntake = 0.1 * self.TotalEnergyExpenditure()
        self.recommendedMinSugarIntake = 0.06 * self.TotalEnergyExpenditure()

    def SugarGramsToCalories(self, gramsSugar):
        return 4 * gramsSugar

    def AppropriateGoals(self, calorieIntake, sugarIntake):
        CI = True
        SI = True
        #People need at least 1200 calories or 60% of daily expenditure.
        if calorieIntake < 0.7 * self.TotalEnergyExpenditure():
            print("Calorie Intake not Appropriate")
            CI = False

        self.SugarIntake()
        if sugarIntake < 0.5 * self.recommendedMinSugarIntake():
            print("Sugar Intake not Appropriate")
            SI = False

        return CI, SI

    def AppropriateGoalsBMI(self, BMI):
        CI = True
        SI = True
        classification = self.BMIClassification(BMI)
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
