import threading

from flask import Flask
from flask import request

import manager

app = Flask(__name__)
manager = manager.Manager()


@app.route('/statement', methods=['GET'])
def output():
    print("Handling Statement")
    return {"outputs": manager.playStatement()}

@app.route('/response', methods=['GET'])
def response():
    response = request.args.get('response')
    print("Handling Response")
    print(response)
    #Send "end" if you want the conversation to go to an end state.
    return {"outputs": manager.handleResponse(response)}

app.run()
