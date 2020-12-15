
class Greeting:
    def __init__(self):
        self.states = [{
            "name": "Greeting",
            "statement": "Hello there, I am diet bot. How are you doing?",
            "response": self.GreetingResponse(),
        },
        {
            "name": "AskName",
            "statement": "What is your name?",
            "response": None
        }]

    def GreetingResponse(self):
        #Process the response here.
        possibleResponses = []
        variables = []
        variableValues = []
        nextState = ""
        return variableValues, nextState