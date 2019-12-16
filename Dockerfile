FROM 119.3.170.97:5000/ubuntu
MAINTAINER xioqiangnobug 15229370298@163.com
WORKDIR /usr/src
RUN sapt-get update -y
RUN apt-get upgrade -y
RUN git clone https://github.com/xiaoqiangnobug/qkflask.git
WORKDIR /usr/src/qkflask/
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
RUN pip install gunicorn -i https://mirrors.aliyun.com/pypi/simple
RUN chomd +x run.sh
CMD /usr/src/qkflask/run.sh