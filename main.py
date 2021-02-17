from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import loads
from json import dumps
import json
import cv2
import face_detection
import numpy as np
import base64

detector = face_detection.build_detector("DSFDDetector", confidence_threshold=.5, nms_iou_threshold=.3) # khởi tạo "model"

producer = KafkaProducer(
    value_serializer=lambda m: dumps(m).encode('utf-8'), 
    bootstrap_servers=['kafka:19091'])
    
def readb64(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

consumer = KafkaConsumer(
    'images',
    bootstrap_servers=['kafka:19091'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:

    message = message.value

    img = readb64(message['imagedata'])
    detections = detector.detect(img)

    # Blue color in BGR 
    color = (255, 0, 0)   
    # Line thickness of 2 px 
    thickness = 3
    # Draw detect box on image
    for face in range(len(detections)):
        pts1 = (detections[face][0],detections[face][1])
        pts2 = (detections[face][2],detections[face][3])

        image = cv2.rectangle(img, pts1, pts2, color, thickness) 
    # rewrite detection image
    cv2.imwrite("detected.png", image)
    with open("detected.png", "rb") as imageFile:
        base64_image = "data:image/png;base64," + base64.b64encode(imageFile.read()).decode("ascii")

    value = {"imagedata": base64_image}

    producer.send("results", value=value)

