import cv2
import time
from threading import Thread

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter


class FaceDetector:
    def __init__(self, camera=0, confidence=0.3):
        self.interpreter = make_interpreter(
            "models/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite"
        )
        self.interpreter.allocate_tensors()
        self.objects = None
        self.confidence = confidence
        self.data = [None, None]
        self.cam = cv2.VideoCapture(camera)
        self.frame = None
        self.stopped = False
        self.quadrant = [0, 0]

    def start(self):
        Thread(target=self.run, args=()).start()
        return self

    def run(self):
        while not self.stopped:
            ret, self.frame = self.cam.read()
            self.frame = cv2.flip(cv2.resize(self.frame, (320, 320)), 1)

            common.set_input(self.interpreter, self.frame)
            self.interpreter.invoke()
            self.objects = detect.get_objects(self.interpreter, self.confidence)

            if len(self.objects) >= 1:
                box = self.objects[0].bbox
                x, y, w, h = (
                    box.xmin,
                    box.ymin,
                    box.xmax - box.xmin,
                    box.ymax - box.ymin,
                )
                imgHeight, imgWidth, _ = self.frame.shape
                centerX = x + w / 2
                centerY = y + h / 2
                if (centerX / imgWidth) < 0.33:
                    self.quadrant = [0, -1]
                elif (centerX / imgWidth) > 0.66:
                    self.quadrant = [0, 1]
                elif (centerY / imgHeight) < 0.33:
                    self.quadrant = [-1, 0]
                elif (centerY / imgHeight) > 0.66:
                    self.quadrant = [1, 0]
                else:
                    self.quadrant = [0, 0]
                print(self.quadrant)
        self.cam.release()

    def getBoundingBoxes(self):
        return self.objects

    def stop(self):
        self.stopped = True


if __name__ == "__main__":
    engine = FaceDetector(camera=2).start()

    time.sleep(1)

    while True:
        frame = engine.frame

        key = cv2.waitKey(10)
        if key == ord("q"):
            break

        boxes = engine.getBoundingBoxes() or []
        for box in boxes:
            box = box.bbox
            x, y, w, h = box.xmin, box.ymin, box.xmax - box.xmin, box.ymax - box.ymin
            imgHeight, imgWidth, _ = frame.shape
            centerX = int(x + w / 2)
            centerY = int(y + h / 2)
            cv2.rectangle(
                frame, (centerX, centerY), (centerX + 3, centerY + 3), (0, 0, 255), 4
            )
        cv2.imshow("frame", frame)
        time.sleep(0.05)
    engine.stop()
