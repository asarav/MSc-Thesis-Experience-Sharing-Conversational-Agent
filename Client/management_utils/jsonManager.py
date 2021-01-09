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

    def writeJSON(self, data, file):
        # WRITING
        with open(file, 'w') as fp:
            json.dump(data, fp, indent=4)