import cv2
import numpy as np
import time
from PIL import Image

from pycoral.adapters import common
from pycoral.adapters import segment
from pycoral.utils.edgetpu import make_interpreter


def create_pascal_label_colormap():
    colormap = np.zeros((256, 3), dtype=int)
    indices = np.arange(256, dtype=int)

    for shift in reversed(range(8)):
        for channel in range(3):
            colormap[:, channel] |= ((indices >> channel) & 1) << shift
        indices >>= 3

    return colormap


def label_to_color_image(label):
    if label.ndim != 2:
        raise ValueError("Expect 2-D input label")

    colormap = create_pascal_label_colormap()

    if np.max(label) >= len(colormap):
        raise ValueError("label value too large.")

    return colormap[label]


class Segmenter:
    def __init__(self):
        self.interpreter = make_interpreter(
            "models/deeplabv3_mnv2_pascal_quant_edgetpu.tflite", device=":0"
        )
        self.interpreter.allocate_tensors()
        self.maskedImage = None

    def inference(self, image):
        resized, _ = common.set_resized_input(
            self.interpreter,
            (image.shape[0], image.shape[1]),
            lambda size: cv2.resize(image, size),
        )
        self.interpreter.invoke()
        result = segment.get_output(self.interpreter)
        if len(result.shape) == 3:
            result = np.argmax(result, axis=-1)
        self.maskedImage = label_to_color_image(result).astype(np.uint8)
        return self.maskedImage

    def getForDisplay(self):
        if self.maskedImage is None:
            return None
        return cv2.resize(self.maskedImage, (20, 15))


if __name__ == "__main__":
    engine = Segmenter()
    cam = cv2.VideoCapture(2)

    while True:
        start = time.time()
        ret, frame = cam.read()
        key = cv2.waitKey(10)
        if key == ord("q"):
            cam.release()
            break
        start = time.time()
        result = engine.inference(frame)
        cv2.imshow("frame", engine.maskedImage)
        print("{:.2f} ms".format((time.time() - start) * 1000))
