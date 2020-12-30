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

    #Gets a state by its unique name in the list of states
    def getState(self, name):
        for state in self.states:
            if state["name"] == name:
                return state

    #Updates the state and parses the response
    def handleResponse(self, response):
        state = self.getState(self.currentStateName)
        variables = []
        #Update new state
        if state["response"] is not None:
            if isinstance(state["response"], str):
                print("Statement!")
                self.currentStateName = state["response"]
            else:
                variables, self.currentStateName = state["response"](response)

        #Get next state type so that Furhat knows what to do.
        nextState = self.getState(self.currentStateName)
        if "stateType" in nextState:
            nextStateType = nextState["stateType"]

        return variables, self.currentStateName, nextStateType

    def caseFolding(self, response):
        return response.casefold()

    def NER(self, response):
        return
