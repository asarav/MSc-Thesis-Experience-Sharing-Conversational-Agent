from dialogue_states.greeting import Greeting
from dialogue_states.session1End import Session1End
from dialogue_states.session1Start import Session1Start
from dialogue_states.session1GoalSetting import Session1GoalSetting
from dialogue_states.session2QuestonsAndEnd import Session2QuestionsAndEnd
from dialogue_states.session2Start import Session2Start
from management_utils.response_manager import ResponseManager
import random


class Manager:
    def __init__(self):
        self.states = []
        self.basicStates = []
        #Set the starting state here.
        self.currentStateName = "AskUserID"
        self.Greeting = Greeting()
        self.session1Start = Session1Start()
        self.session1GoalSetting = Session1GoalSetting()
        self.session1End = Session1End()
        self.session2Start = Session2Start()
        self.session2QuestionsAndEnd = Session2QuestionsAndEnd()
        self.states = self.states + \
                      self.Greeting.states + \
                      self.session1Start.states + \
                      self.session1GoalSetting.states +\
                      self.session1End.states +\
                      self.session2Start.states +\
                      self.session2QuestionsAndEnd.states
        self.responseManager = ResponseManager()
        self.repeat = False

    #Expects either a string or a function that returns a string.
    def playStatement(self):
        state = self.getState(self.currentStateName)
        statement = ""
        if isinstance(state["statement"], str):
            statement = state["statement"]
        else:
            statement = state["statement"]()

        if self.repeat:
            self.repeat = False
            #Choose initial statement.
            initial = random.choice(["Okay. ", "I will repeat that. ", "Sure. "])
            statement = initial + statement
        else:
            #Add voice gestures if not repeating
            statement = self.responseManager.AddVoiceGestures(statement)
            print("Voice Gestures Added")


        return statement

    def getGesture(self):
        state = self.getState(self.currentStateName)
        gesture = None
        # Where 0 is before and 1 is after.
        gestureTiming = False
        if "gesture" in state:
            gesture = state["gesture"]
        if "gestureTiming" in state:
            gestureTiming = state["gestureTiming"]
        return gesture, gestureTiming



    #Gets a state by its unique name in the list of states
    def getState(self, name):
        for state in self.states:
            if state["name"] == name:
                return state

    #Updates the state and parses the response
    def handleResponse(self, response):
        state = self.getState(self.currentStateName)
        response = response.strip('"')
        variables = []
        #Update new state
        if self.responseManager.AskRepeat(response):
            self.currentStateName = state["name"]
            self.repeat = True
        elif state["response"] is not None:
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
