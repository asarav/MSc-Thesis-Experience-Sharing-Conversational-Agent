from dialogue_states.greeting import Greeting


class Manager:
    def __init__(self):
        self.states = []
        self.basicStates = []
        #Set the starting state here.
        self.currentStateName = "AskUserID"
        self.Greeting = Greeting()
        self.states = self.states + self.Greeting.states

    #Expects either a string or a function that returns a string.
    def playStatement(self):
        state = self.getState(self.currentStateName)
        if isinstance(state["statement"], str):
            return state["statement"]
        else:
            return state["statement"]()

    def getState(self, name):
        for state in self.states:
            if state["name"] == name:
                return state

    def handleResponse(self, response):
        state = self.getState(self.currentStateName)
        variables = []
        if state["response"] is not None:
            variables, self.currentStateName = state["response"](response)

        nextState = self.getState(self.currentStateName)
        if "stateType" in nextState:
            nextStateType = nextState["stateType"]

        return variables, self.currentStateName, nextStateType

    def caseFolding(self, response):
        return response.casefold()

    def NER(self, response):
        return
