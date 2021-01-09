# Python program to demonstrate
# Conversion of JSON data to
# dictionary


# importing the module
import json

data = {}

class jsonManager:
    def __init__(self):
        # READING
        # Opening JSON file
        self.data = {}

    def readJSON(self, file):
        with open(file) as json_file:
            self.data = json.load(json_file)

            # Print the type of data variable
            print("Type:", type(data))

            # Print the data of dictionary
            print("\nPeople1:", data['people1'])
            print("\nPeople2:", data['people2'])

    def writeJSON(self, data, file):
        # WRITING
        with open(file, 'w') as fp:
            json.dump(data, fp, indent=4)