#coding:utf-8
from ultralytics import YOLO

# 加载预训练模型
model = YOLO("yolov8n-cls.pt")
if __name__ == '__main__':
    model.train(data='datasets/ExpressionData', epochs=300, batch=4)
    # results = model.val()
    # # results = model("自己的验证图片")


