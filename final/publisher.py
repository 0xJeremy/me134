import zmq
import cv2
import base64

ADDRESS = "172.20.10.2"
PORT = 8484
TOPIC = "\0\0\0 ".encode()


class Publisher:
    def __init__(self, address=ADDRESS, port=PORT):
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.setsockopt(zmq.SNDHWM, 1) # set the high water mark to 1 frame
        self.publisher.bind("tcp://{}:{}".format(address, port))

    def sendImage(self, image):
        self.publisher.send(TOPIC + base64.b64encode(cv2.imencode(".png", image)[1]))


if __name__ == "__main__":
    from camera import Camera
    import time

    publisher = Publisher()
    camera = Camera(callback=publisher.sendImage).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        camera.stop()
