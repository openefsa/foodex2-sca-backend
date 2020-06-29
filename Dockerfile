FROM python:3.7.4

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
RUN mkdir -p /app/src/delaware_models
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
# RUN python -c "import nltk;nltk.download('stopwords')"
# RUN python -c "import nltk;nltk.download('punkt')"

WORKDIR /app
COPY . /app
CMD ["flask", "run", "--host=0.0.0.0"]
