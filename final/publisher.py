import zmq
import cv2
import base64

ADDRESS = "127.0.0.1"
PORT = 8484
TOPIC = "\0\0\0 ".encode()


class Publisher:
    def __init__(self, address=ADDRESS, port=PORT):
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind("tcp://{}:{}".format(address, port))

    def sendImage(self, image):
        self.publisher.send(TOPIC + base64.b64encode(cv2.imencode(".png", image)[1]))


if __name__ == "__main__":
    from camera import Camera
    import time

    publisher = Publisher()
    camera = Camera(camera=2, callback=publisher.sendImage).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        camera.stop()
