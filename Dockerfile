# syntax=docker/dockerfile:1

FROM python:3.7.12-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
      bzip2 \
      g++ \
      git \
      graphviz \
      libgl1-mesa-glx \
      libhdf5-dev \
      openmpi-bin \
      wget \
      python3-tk && \
    rm -rf /var/lib/apt/lists/*

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

# CMD ["python3", "--image_dir ./demo", "--image_format jpeg", "--prefix M30_", "--square_size 0.025", "--width 9", "--height 6", "--save_file M30_calibration.yml"]