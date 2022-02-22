# syntax=docker/dockerfile:1

FROM python:3.7.12-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
     libglib2.0-0 libsm6 libxrender1 libxext6 && \
     rm -rf /var/lib/apt/lists/*

RUN mkdir /calibration
WORKDIR /calibration

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Minimize image size 
RUN (apt-get autoremove -y; \
     apt-get autoclean -y)  

ENV QT_X11_NO_MITSHM=1

CMD ["bash"]