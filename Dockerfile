FROM python:alpine as test

COPY ./backend                   /app
COPY ./backend/repositories      /etc/apk/repositories
COPY ./backend/pip.conf          /root/.pip/pip.conf
RUN apk --no-cache --verbose add musl-dev openssl-dev libffi-dev pcre-dev postgresql-dev gcc \
    && pip install pipenv \
    && cd /app \
    && pipenv install --system --deploy --dev \
    && flake8 \
    && cd /app/test \
    && python -m unittest


FROM node:alpine as node

COPY ./frontend                  /app/

WORKDIR /app

ARG npm_registry=https://registry.npm.taobao.org

RUN npm install -g @angular/cli --registry=${npm_registry} \
    && npm install --registry=${npm_registry} \
    && ng build --prod --output-path=./dist


FROM python:alpine

COPY ./backend                   /app
COPY ./backend/repositories      /etc/apk/repositories
COPY ./backend/pip.conf          /root/.pip/pip.conf
COPY backend/nginx_main.nginx   /etc/nginx/nginx.conf
COPY backend/nginx_sub.nginx    /etc/nginx/conf.d/default.conf
COPY --from=node /app/dist     /var/www/blog/

# TODO remove -dev packages

RUN apk --no-cache --verbose add musl-dev openssl-dev libffi-dev pcre-dev postgresql-dev gcc nginx \
    && pip install pipenv \
    && cd /app \
    && pipenv install --system --deploy \
    && apk --purge --verbose del gcc \
    && mkdir -p /run/nginx

EXPOSE 80

CMD ["supervisord", "-c", "/app/supervisord.conf"]
