FROM rauliu/ubuntu-dev
MAINTAINER xioqiangnobug 15229370298@163.com
WORKDIR /usr/src
RUN sudo apt-get update
RUN sudo sudo apt-get upgrade
RUN git clone https://github.com/xiaoqiangnobug/qkflask.git
WORKDIR /usr/src/qkflask
RUN pip install -r requesments.txt -i https://mirrors.aliyun.com/pypi/simple
RUN pip install gunicorn -i https://mirrors.aliyun.com/pypi/simple
RUN chomd +x run.sh
CMD /usr/src/qkflask/run.sh