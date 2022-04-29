FROM python:3.8.13-alpine3.15
RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
	apk add --no-cache --update python3 && \
	pip3 install --upgrade pip setuptools
RUN pip3 install pendulum service_identity
# Tell Python to not generate .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Turn off buffering
ENV PYTHONUNBUFFERED 1

RUN pip install PyMySQL
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app
ADD . /app
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
# CMD ["python", "main.py"]