import zmq
import cv2
import base64
import numpy as np

ADDRESS = "172.20.10.2"
PORT = 8484
TOPIC = "\0\0\0"


class Subscriber:
    def __init__(self, address=ADDRESS, port=PORT):
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect("tcp://{}:{}".format(address, port))
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, TOPIC)

    def recv(self):
        rawMessage = self.subscriber.recv()
        topic, encodedImage = rawMessage.split()
        return cv2.imdecode(
            np.frombuffer(base64.b64decode(encodedImage), dtype=np.uint8),
            cv2.IMREAD_ANYCOLOR,
        )


if __name__ == "__main__":
    subscriber = Subscriber()

    while True:
        image = subscriber.recv()
        cv2.imshow("Frame", cv2.flip(image, -1))
        key = cv2.waitKey(100) & 0xFF
        if key == ord("q"):
            break
