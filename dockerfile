FROM python:3.8.5-slim-buster

EXPOSE 30000
VOLUME [ "/app/runtime", "/app/config" ]
WORKDIR /app

COPY ./ /app/
RUN cp /usr/share/zoneinfo/PRC /etc/localtime && \
    pip install --no-cache-dir -r /app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

ENTRYPOINT [ "python", "app.py" ]
