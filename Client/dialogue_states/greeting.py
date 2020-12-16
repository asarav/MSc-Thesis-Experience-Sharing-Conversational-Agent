
class Greeting:
    def __init__(self):
        self.states = [{
            "name": "Greeting",
            "statement": "Hello there, I am diet bot. How are you doing?",
            "response": self.GreetingResponse,
            "stateType": "AnswerResponse"
        },
        {
            "name": "AskName",
            "statement": "What is your name?",
            "response": None,
            "stateType": "End"
        }]

    def GreetingResponse(self, response):
        #Process the response here.
        nextState = "AskName"
        return [], nextState