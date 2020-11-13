import zmq
import json
import time

ADDRESS = '172.20.10.3'
PORT = 8484

class Sender:
    def __init__(self, address=ADDRESS, port=PORT):
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PAIR)
        try:
            self.publisher.bind('tcp://{}:{}'.format(address, port))
        except:
            print("Binding to localhost...")
            self.publisher.bind('tcp://{}:{}'.format('127.0.0.1', port))

    def send(self, locations):
        toSend = json.dumps(locations)
        print("Sending", toSend)
        self.publisher.send_string(toSend)


if __name__ == '__main__':
    import random
    sender = Sender()

    def num():
        return random.randint(1,101)

    while True:
        sender.send([num(), num()])
        time.sleep(0.01)
