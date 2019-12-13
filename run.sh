#!/usr/bin/env bash
cd /usr/src/qkflask
git pull
pip install -r requesments.txt -i https://mirrors.aliyun.com/pypi/simple
gunicorn -w 1 -b 0.0.0.0:5000 app:app