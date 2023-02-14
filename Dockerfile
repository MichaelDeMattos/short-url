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

# Run App
WORKDIR /short-url/src
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["/short-url/wait-for-it.sh -h db -p 5432 --strict --timeout=300 -- \
      /short-url/wait-for-it.sh -h redis -p 6379 --strict --timeout=300 -- \
      /short-url/src/migrations.sh && \
      uwsgi --ini short-url.ini"]
