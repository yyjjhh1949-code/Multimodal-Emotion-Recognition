#coding:utf-8
import cv2
from ultralytics import YOLO
import numpy as np
import detect_tools as tools
import Config

def face_detect(image, face_model):
    # 进行人脸检测，并截取人脸图片
    image = image.copy()
    results = face_model(image, conf=0.5)
    face = []
    face_locations = []
    if len(results[0].boxes.data):
        face_locations_float = results[0].boxes.xyxy.tolist()
        for each in face_locations_float:
            face_locations.append(list(map(int, each)))
        for face_location in face_locations:
            left, top, right, bottom = face_location
            face.append(image[top:bottom, left:right])
            image = cv2.rectangle(image, (left, top), (right, bottom), (50, 50, 250), 3)
        return image, face, face_locations
    else:
        return image, None, None


# 所需加载的模型目录
face_model_path = 'models/yolov8n-face.pt'
expression_model_path = 'models/expression_cls.pt'
# 人脸检测模型
face_model = YOLO(face_model_path, task='detect')
# 表情识别模型
expression_model = YOLO(expression_model_path, task='classify')

cap = cv2.VideoCapture(0)
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        face_cvimg, faces, locations = face_detect(frame, face_model)

        if faces is not None:
            for i in range(len(faces)):
                left, top, right, bottom = locations[i]
                # 彩色图片变灰度图
                img = cv2.cvtColor(faces[i], cv2.COLOR_BGR2GRAY)
                # 灰度图变3通道
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
                rec_res = expression_model(img)
                probs = rec_res[0].probs.data.tolist()
                num = np.argmax(probs)
                label = Config.names[num]
                face_cvimg = cv2.putText(face_cvimg, label, ((left, top - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                         (0, 0, 250),
                                         2, cv2.LINE_AA)
        cv2.imshow('yolov8_detections', face_cvimg)
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()