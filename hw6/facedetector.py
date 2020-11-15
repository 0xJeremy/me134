import cv2
import time

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

class FaceDetector:
	def __init__(self, confidence=0.5):
		self.interpreter = make_interpreter('models/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite')
		self.interpreter.allocate_tensors()
		self.objects = None
		self.confidence = confidence
		self.data = [None, None]

	def detect(self, image):
		common.set_input(self.interpreter, image)
		self.interpreter.invoke()
		self.objects = detect.get_objects(self.interpreter, self.confidence)
		if self.objects and self.objects[0]:
			box1 = self.objects[0].bbox
			pos1 = (box1.ymin + box1.ymax) / 2 / image.shape[1]
			if len(self.objects) == 2:
				box2 = self.objects[1].bbox
				pos2 = (box2.ymin + box2.ymax) / 2 / image.shape[1]

				if box1.xmin < box2.xmin:
					self.data = [pos1, pos2]
				else:
					self.data = [pos2, pos1]
			else:
				self.data = [pos1, None]

	def getBoundingBoxes(self):
		return self.objects

if __name__ == '__main__':
	engine = FaceDetector()
	cam = cv2.VideoCapture(2)

	while True:
		start = time.time()
		ret, frame = cam.read()
		frame = cv2.resize(frame, (320, 320))
		key = cv2.waitKey(10)
		if key == ord('q'):
			cam.release()
			break
		start = time.time()
		engine.detect(frame)
		boxes = engine.getBoundingBoxes()
		for box in boxes:
			box = box.bbox
			box = [box.xmin, box.ymin, box.xmax, box.ymax]
			cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255,0,0), 2)
		if engine.data[0] is not None:
			pos = int(engine.data[0] * frame.shape[1])
			cv2.rectangle(frame, (20, pos), (30, pos+10), (0, 0, 255))
		cv2.imshow("frame", frame)
		print("{:.2f} ms".format((time.time()-start)*1000))
