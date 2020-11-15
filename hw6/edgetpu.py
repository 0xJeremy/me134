import cv2
import time

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

class face_detection:
	def __init__(self):
		self.interpreter = make_interpreter('models/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite')
		self.interpreter.allocate_tensors()
		self.objects = None

	def detect(self, image):
		common.set_input(self.interpreter, image)
		self.interpreter.invoke()
		self.objects = detect.get_objects(self.interpreter, 0.5)
		print(self.objects)

	def get_bounding_boxes(self):
		return self.objects

if __name__ == '__main__':
	engine = face_detection()
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
		boxes = engine.get_bounding_boxes()
		for box in boxes:
			box = box.bbox
			box = [box.xmin, box.ymin, box.xmax, box.ymax]
			cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255,0,0), 2)
		cv2.imshow("frame", frame)
		print("{:.2f} ms".format((time.time()-start)*1000))
