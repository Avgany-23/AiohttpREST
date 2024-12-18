FROM python:3.12.0-alpine AS builder

LABEL author='avgany'

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update &&  \
    apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip

COPY requirements.txt /usr/src/app
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


FROM python:3.12.0-alpine

LABEL author='avgany'

ENV HOME=/home/app
ENV APP_HOME=/home/app/website

RUN mkdir -p $APP_HOME \
    && addgroup -S app \
    && adduser -S app -G app \
    && apk update \
    && apk add libpq \
    && chown -R app:app $APP_HOME \
    && chmod -R 755 $APP_HOME

COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

WORKDIR $APP_HOME

COPY . .

RUN chmod +x docker.sh

CMD sh docker.sh
