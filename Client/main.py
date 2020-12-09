import threading

from flask import Flask

import manager

app = Flask(__name__)
manager = manager.manager()


@app.route('/output')
def hello_world():
    print("Sending predictions")
    return {"outputs": manager.get_and_empty_outputs()}


if __name__ == "__main__":
    threading.Thread(target=app.run).start()
    manager.start_loop()
