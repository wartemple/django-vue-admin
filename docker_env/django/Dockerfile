FROM python:3.8.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# 容器内创建 app 文件夹
ENV APP_HOME=/app
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# COPY pip.conf /root/.pip/pip.conf
COPY /backend/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -U pip wheel &&\
    pip install --no-cache-dir -r /tmp/requirements.txt

# 将当前目录加入到工作目录中 (. 表示当前目录)
COPY ./backend/ ${APP_HOME}

# 启动
ENTRYPOINT [ "/bin/bash" ]

CMD ["/app/docker_start.sh"]
