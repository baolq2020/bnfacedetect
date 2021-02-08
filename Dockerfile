FROM python:3.6.1-alpine
RUN apk update
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
RUN pip install --upgrade pip
# RUN pip install face-detection
# RUN pip install cv2
RUN pip install kafka

CMD [ "python", "./main.py" ]