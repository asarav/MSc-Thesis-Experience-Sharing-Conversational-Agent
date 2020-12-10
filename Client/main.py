import threading

from flask import Flask

import manager

app = Flask(__name__)
manager = manager.Manager()


@app.route('/statement')
def output():
    print("Sending predictions")
    print(manager.get_and_empty_outputs())
    return {"outputs": "statement"}

@app.route('/response')
def response():
    print("Sending predictions")
    print(manager.get_and_empty_outputs())
    return {"outputs": "HI"}

app.run()
