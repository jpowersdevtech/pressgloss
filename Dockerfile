#First phase for AMR dependencies. 
# first stage
FROM nvidia/cuda:11.1-base-ubuntu18.04 as builder
RUN apt-get update && apt-get install -y curl wget gcc build-essential

# install conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.5.12-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

# create env with python 3.6
RUN /opt/conda/bin/conda create -y -n myenv python=3.6.15
    
# install requirements
WORKDIR /app
COPY AMR/umd_requirements.txt /app
ENV PATH=/opt/conda/envs/myenv/bin:$PATH    
RUN pip install -r AMR/umd_requirements.txt
RUN pip uninstall -y pip

#Second phaseibhjuy

FROM alpine:latest
RUN apk update

RUN apk add py-pip
RUN apk add --no-cache python3-dev
RUN pip install --upgrade pip

WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 5000

ENTRYPOINT []

CMD ["python3", "-m", "pressgloss", "--operation", "app"]
