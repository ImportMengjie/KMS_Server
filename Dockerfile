# FROM ubuntu:16.04
# RUN apt update
# RUN apt install -y python3
# RUN apt update --fix-missing
# RUN apt install -y python3-pip
# RUN apt install -y curl
# RUN pip3 install flask
# WORKDIR ~/
# RUN curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-3.6.3.tgz

# FROM kms:v0.1
# RUN tar -zxvf mongodb-linux-x86_64-ubuntu1604-3.6.3.tgz
# RUN mv  mongodb-linux-x86_64-ubuntu1604-3.6.3/ /usr/local/mongodb       
# RUN export PATH=/usr/local/mongodb/bin:$PATH
# RUN mkdir -p /data/dbro

FROM kms:v0.2
WORKDIR /app
COPY ./* /app/
RUN pip3 install -r requirements.txt