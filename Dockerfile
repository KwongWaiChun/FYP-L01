FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python3 -m venv venv
RUN venv/bin/pip3 install --upgrade pip
RUN venv/bin/pip3 install -r requirements.txt

COPY app app
COPY migrations migrations
COPY run.py run.py

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs

EXPOSE 443

CMD ["venv/bin/python3", "run.py"]