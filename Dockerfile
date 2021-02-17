FROM python:3.8

RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
RUN pip install --upgrade pip
RUN pip install opencv-python
RUN pip install face-detection
RUN pip install kafka-python

CMD [ "python", "./main.py" ]