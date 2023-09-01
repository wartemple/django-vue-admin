FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /backend
COPY ./backend/ .
RUN awk 'BEGIN { cmd="cp -i ./conf/env.example.py   ./conf/env.py "; print "n" |cmd; }'
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
CMD ["/backend/docker_start.sh"]
