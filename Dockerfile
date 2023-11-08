FROM python:3.9.1-slim-buster
VOLUME /data
EXPOSE 8000
ENV TZ=Asia/Shanghai \
    PYTHONPATH="${PYTHONPATH}:/dependencies:/app" \
    WORKDIR='/data' \
    MEM_API_KEY='' \
    CUBOX_AUTH_CODE='' \
    CUBOX_SYNC_INTERVAL=300

COPY app /app
COPY memflow /app/memflow
COPY requirements.txt /

RUN apt-get -y update \
	&& apt-get install -y --no-install-recommends tzdata \
    && python -m pip install --upgrade pip \
    && pip install supervisor \
    && pip install --target=/dependencies -r requirements.txt \
	&& ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime  \
	&& echo ${TZ} > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
CMD sh /app/start.sh
