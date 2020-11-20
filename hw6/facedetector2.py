from threading import Thread
import cv2


class FaceDetector:
    def __init__(self, camera=0):
        self.stopped = False
        self.cam = cv2.VideoCapture(camera)
        self.faceCascade = cv2.CascadeClassifier("models/haarcascade_eye.xml")
        self.frame = None
        self.faces = None
        self.quadrant = [0, 0]

    def start(self):
        Thread(target=self.run, args=()).start()
        return self

    def run(self):
        while not self.stopped:
            ret, self.frame = self.cam.read()
            self.faces = self.faceCascade.detectMultiScale(
                self.frame, scaleFactor=1.1, minNeighbors=3, minSize=(20, 20),
            )
            # print(self.faces)
            if len(self.faces) >= 1:
                x, y, w, h = self.faces[0]
                imgHeight, imgWidth, _ = self.frame.shape
                centerX = x + w / 2
                centerY = y + h / 2
                if (centerX / imgWidth) < 0.33:
                    self.quadrant = [0, 1]
                elif (centerX / imgWidth) > 0.66:
                    self.quadrant = [0, -1]
                elif (centerY / imgHeight) < 0.33:
                    self.quadrant = [-1, 0]
                elif (centerY / imgHeight) > 0.66:
                    self.quadrant = [1, 0]
                else:
                    self.quadrant = [0, 0]
        self.cam.release()

    def stop(self):
        self.stopped = True


if __name__ == "__main__":
    import time

    detector = FaceDetector(camera=2).start()
    time.sleep(1)

    while True:
        frame = detector.frame
        imgHeight, imgWidth, _ = frame.shape
        for (x, y, w, h) in detector.faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            centerX = int(x + w / 2)
            centerY = int(y + h / 2)
            cv2.rectangle(
                frame, (centerX, centerY), (centerX + 3, centerY + 3), (0, 0, 255), 4
            )

        print(detector.quadrant)
        cv2.imshow("Faces!", cv2.flip(frame, 1))
        key = cv2.waitKey(5) & 0xFF
        if key == ord("q"):
            break
        time.sleep(0.05)
    detector.stop()
