import threading

from flask import Flask
from flask import request

import manager

app = Flask(__name__)
manager = manager.Manager()


@app.route('/statement', methods=['GET'])
def output():
    print("Handling Statement")
    statement = manager.playStatement()
    package = {"outputs": statement, "gesture": "None", "gestureTiming": "None"}
    gesture, gestureTiming = manager.getGesture()
    if gesture is not None:
        package["gesture"] = gesture
    if gestureTiming is not None:
        package["gestureTiming"] = gestureTiming
    return package

@app.route('/response', methods=['GET'])
def response():
    response = request.args.get('response')
    print("Handling Response")
    #Send "end" if you want the conversation to go to an end state.
    _,_,stateType = manager.handleResponse(response)
    return {"outputs": stateType}

app.run()
