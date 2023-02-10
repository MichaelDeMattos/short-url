FROM python:3.10.1

RUN apt update \
    && apt install libpq-dev gcc -y \
    && pip install --upgrade pip

WORKDIR /short-url/src

# Copy
COPY ./requirements.txt /short-url/requirements.txt
COPY ./wait-for-it.sh /short-url/wait-for-it.sh
RUN pip install -r /short-url/requirements.txt
RUN chmod +x /short-url/wait-for-it.sh
COPY . /short-url/

# Flask Env
ENV FLASK_DEBUG 1
ENV FLASK_SECRETKEY your_secret_key

WORKDIR /short-url/src
