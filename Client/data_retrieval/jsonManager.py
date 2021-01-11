import json
import os


class jsonManager:
    def __init__(self):
        # READING
        # Opening JSON file
        self.data = {}

    def readJSON(self, file):
        fileExists = False
        if os.path.isfile(file) and os.access(file, os.R_OK):
            # checks if file exists
            print("File exists and is readable")
            fileExists = True
            with open(file) as json_file:
                self.data = json.load(json_file)
        return fileExists

    def writeJSON(self, data, file):
        # WRITING
        with open(file, 'w') as fp:
            json.dump(data, fp, indent=4)

    def writeDataToJSON(self, file):
        # WRITING
        with open(file, 'w') as fp:
            json.dump(self.data, fp, indent=4)