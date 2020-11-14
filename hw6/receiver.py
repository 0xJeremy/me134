import zmq
import json
import time
from threading import Thread

ADDRESS = "172.20.10.3"
PORT = 8484


class Receiver:
    def __init__(self, address=ADDRESS, port=PORT):
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.PAIR)
        self.subscriber.connect("tcp://{}:{}".format(address, port))
        self.stopped = False
        self.data = [None, None]

    def start(self):
        Thread(target=self.run, args=()).start()
        return self

    def run(self):
        while not self.stopped:
            data = self.subscriber.recv()
            jsonData = json.loads(data)
            if jsonData[1] != None:
                self.data = jsonData
            elif jsonData[0] != None:
                self.data = [jsonData[0], None]

    def stop(self):
        self.stopped = True


if __name__ == "__main__":
    receiver = Receiver().start()

    try:
        while True:
            print("Received", receiver.data)
            time.sleep(0.01)
    except:
        receiver.stop()
