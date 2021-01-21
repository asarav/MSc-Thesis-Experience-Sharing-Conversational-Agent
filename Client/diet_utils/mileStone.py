from diet_utils.nutrition import Nutrition


class MileStone:
    def __init__(self, age, weight, height, gender):
        self.nutrition = Nutrition(age, weight, height, gender)

    #Generate milestone and final goal based on nutrition information. This does not handle appropriate goals.
    def generateGoalPlan(self, goal, current):
        if goal is 0:
            TTE = self.nutrition.TotalEnergyExpenditure()
            diff = abs(TTE - current)
            #Set goal for 10% reduction
            finalGoal = current * 0.9
            if finalGoal < 0.7 * TTE:
                finalGoal = 0.7 * TTE
            #Milestone is the halfway point
            milestone = current - (current - finalGoal)/2
            print("Calorie Restriction")
            return finalGoal, milestone
        else:
            finalGoal = current * 0.9
            milestone = current - (current - finalGoal)/2
            print("Sugar reduction")
            return finalGoal, milestone
