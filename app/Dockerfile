FROM python:3.9.10-alpine3.15
RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
	apk add --no-cache --update python3 && \
	pip3 install --upgrade pip setuptools
RUN pip3 install pendulum service_identity

WORKDIR /app

ENV FLASK_ENV production

RUN pip install PyMySQL
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]