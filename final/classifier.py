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
        outputDetails = interpreter.get_output_details()[0]
        output = np.squeeze(interpreter.get_tensor(outputDetails["index"]))
        if outputDetails["dtype"] == np.uint8:
            scale, zero_point = outputDetails["quantization"]
            output = scale * (output - zero_point)
        ordered = np.argpartition(-output, topK)
        return [(i, output[i]) for i in ordered[:topK]]
