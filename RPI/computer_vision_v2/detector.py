import cv2
import numpy as np
import tensorflow as tf

PERSON_CLASS_ID = 0

class HumanDetector:
    def __init__(self, model_path, conf_th=0.3, nms_th=0.4):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.inp = self.interpreter.get_input_details()[0]
        self.out = self.interpreter.get_output_details()[0]

        self.conf_th = conf_th
        self.nms_th = nms_th
        self.is_uint8 = self.inp['dtype'] == np.uint8

    def preprocess(self, frame):
        img = cv2.resize(frame, (320, 320))

        if self.is_uint8:
            return img[None].astype(np.uint8)

        img = img[..., ::-1].astype(np.float32) / 255.0
        return img[None]

    def detect(self, frame):
        h, w = frame.shape[:2]

        inp = self.preprocess(frame)
        self.interpreter.set_tensor(self.inp['index'], inp)
        self.interpreter.invoke()

        output = self.interpreter.get_tensor(self.out['index'])[0].T

        class_scores = output[:, 4:]
        class_ids = np.argmax(class_scores, axis=1)
        scores = np.max(class_scores, axis=1)

        mask = (scores > self.conf_th) & (class_ids == PERSON_CLASS_ID)
        output = output[mask]
        scores = scores[mask]

        if len(output) == 0:
            return []

        cx, cy, bw, bh = output[:, 0], output[:, 1], output[:, 2], output[:, 3]

        x = (cx - bw / 2) * w
        y = (cy - bh / 2) * h
        bw *= w
        bh *= h

        boxes = np.stack([x, y, bw, bh], axis=1).astype(int).tolist()
        scores = scores.tolist()

        indices = cv2.dnn.NMSBoxes(boxes, scores, self.conf_th, self.nms_th)

        if len(indices) == 0:
            return []

        return [boxes[i] for i in np.array(indices).flatten()]