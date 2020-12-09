from tflite_runtime.interpreter import Interpreter
import cv2
import numpy as np


def loadLabels(path):
    with open(path, "r") as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}


def setInputTensor(interpreter, image):
    tensorIndex = interpreter.get_input_details()[0]["index"]
    inputTensor = interpreter.tensor(tensorIndex)()[0]
    inputTensor[:, :] = image


class Classifier:
    def __init__(self, modelPath="course_classifier.tflite", labels="labels.txt"):
        self.interpreter = Interpreter(modelPath)
        self.interpreter.allocate_tensors()
        _, self.height, self.width, _ = self.interpreter.get_input_details()[0]["shape"]
        self.result = None
        self.labels = loadLabels(labels)

    def classify(self, image, topK=1):
        image = cv2.resize(image, (self.height, self.width))
        setInputTensor(self.interpreter, image)
        self.interpreter.invoke()
        outputDetails = self.interpreter.get_output_details()[0]
        output = np.squeeze(self.interpreter.get_tensor(outputDetails["index"]))
        ordered = np.argpartition(-output, topK)
        # print(self.labels[ordered[0]])
        print(ordered)
        return [(i, output[i]) for i in ordered[:topK]]


if __name__ == "__main__":
    classifier = Classifier()

    cam = cv2.VideoCapture(2)

    while True:
        ret, frame = cam.read()
        results = classifier.classify(frame)
        print(results)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(100) & 0xFF
        if key == ord("q"):
            break

    cam.release()
