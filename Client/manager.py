from threading import Thread
from typing import Optional
from dialogue_states.greeting import Greeting


class Manager:
    def __init__(self):
        self.states = []
        self.currentStateName = "Greeting"
        self.Greeting = Greeting()
        self.states.push(self.Greeting.states)

    def playStatement(self):
        state = self.getState(self.currentStateName)
        return state["statement"]

    def getState(self, name):
        for state in self.states:
            if state["name"] == name:
                return state

    def handleResponse(self):
        state = self.getState(self.currentStateName)
        return state["response"]()
