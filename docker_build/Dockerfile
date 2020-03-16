FROM python:3

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /doc/requirements.txt

WORKDIR /

RUN pip install -r requirements.txt

COPY . /

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]