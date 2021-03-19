from os import listdir
from os.path import isfile, join

import data_retrieval.jsonManager
import management_utils.response_manager

RM = management_utils.response_manager.ResponseManager()

id = input("Enter userid: ")
#Make id all caps
id = str(id).upper()
print("Userid is: " + id)
name = input("Enter name: ")
print("Name is: " + name)
gender = input("Enter gender: ")
gd = RM.DetermineGender(gender)
if gd is 0:
    gender = "female"
else:
    gender = "male"
print("Gender is: " + gender)
ProlificID = input("Enter prolificid: ")
ProlificID = str(ProlificID).upper()
if ProlificID == "NONE":
    ProlificID = None
print("ProlificID is: " + str(ProlificID))
age = input("Enter age: ")
age = int(age)
print("Age is: " + str(age))
weight = input("Enter weight: ")
weight = int(weight)
print("Weight is: " + str(weight))
height = input("Enter height: ")
height = int(height)
print("Height is: " + str(height))

#Get Condition?

#Create json file
manager = data_retrieval.jsonManager.jsonManager()
manager.data["id"] = id
manager.data["generated"] = True
manager.data["name"] = name
manager.data["prolificid"] = ProlificID
manager.data["physicalData"] = {
    "gender": gender,
    "age": age,
    "weight": weight,
    "height": height
}
manager.data["session"] = 1

file = "interaction_data/" + str(id) + ".json"
manager.writeDataToJSON(file)