FROM certbot/certbot:latest AS base-amd64
FROM certbot/certbot:arm32v6-latest AS base-arm

FROM base-${TARGETARCH}

RUN apk add --no-cache nginx supervisor bash jq

COPY . /tmp/dynname-proxy
RUN pip3 install --no-cache /tmp/dynname-proxy j2cli
RUN apk add --no-cache gcc musl-dev linux-headers && \
    pip3 install --no-cache psutil && \
    apk del gcc musl-dev linux-headers

RUN mkdir -p /opt/dynname/data && \
    mkdir -p /opt/dynname/conf && \
    cp -fr /tmp/dynname-proxy/bin /opt/dynname/ && \
    chmod +x -R /opt/dynname/bin && \
    cp /tmp/dynname-proxy/conf/supervisord.conf /etc/supervisord.conf && \
    crontab -c /etc/crontabs/ /tmp/dynname-proxy/conf/crontab &&  \
    cp /tmp/dynname-proxy/conf/proxy.conf /etc/nginx/proxy.conf && \
    cp /tmp/dynname-proxy/conf/nginx.conf.j2 /opt/dynname/conf/

ENV CONFIG_PATH=/opt/dynname/data/.dynname.json \
    UPSTREAM_HTTP_HOST=upstream \
    UPSTREAM_HTTP_PORT=80 \
    UPSTREAM_HTTPS_HOST=upstream \
    UPSTREAM_HTTPS_PORT=443

EXPOSE 80 443

VOLUME ["/opt/dynname/data"]

ENTRYPOINT []
CMD ["/opt/dynname/bin/start"]
