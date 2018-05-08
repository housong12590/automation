#!/usr/bin/env bash

docker run -d --name chaos \
                --restart always \
                -e MODE=dev \
                -e SECRET_KEY='m&!rab9w$3ji%4*8ifqy@hy^*49eaxj=@atzlwvupcr)b5s41z' \
                -e MYSQL_HOST=192.168.0.211 \
                -e MYSQL_PORT=3307 \
                -e MYSQL_USER=root \
                -e MYSQL_PASSWORD=123456 \
                -e MYSQL_PASSWORD=123456 \
                -e MYSQL_PASSWORD=123456 \
                -e MYSQL_PASSWORD=123456 \
                -e MYSQL_PASSWORD=123456 \
                -e MYSQL_PASSWORD=123456 \
                -e MYSQL_PASSWORD=123456 \
                -e MYSQL_PASSWORD=123456 \
                -e MYSQL_PASSWORD=123456 \
                -e MYSQL_PASSWORD=123456 \
                -e MYSQL_PASSWORD=123456 \
                -e MYSQL_DB=tcmipr_dev \
                -e SENTRY_DSN='https://0ccf2691192743eaa9dc777e932e14ff:f04dce4f5b9344e2841959841a7b3ef5@error.jiankanghao.net/23' \
                -p 9393:5000 192.168.0.210/haiwei/chaos