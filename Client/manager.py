from threading import Thread
from typing import Optional

class Manager:

    def __init__(self):
        self.outputs = []

    def get_and_empty_outputs(self):
        to_return = self.outputs
        self.outputs = []
        return to_return

    def start_loop(self):
        images = []
        t: Optional[Thread] = None
        while True:
            print("Hi")