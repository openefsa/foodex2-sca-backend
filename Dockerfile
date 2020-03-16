FROM python:3.7.4

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
RUN mkdir -p /app/src
ADD https://efsapublicmodels.blob.core.windows.net/efsapublicmodels/FOODEX/foodex2PreditionDeployed.zip /app
RUN unzip /app/foodex2PreditionDeployed.zip -d /tmp/
RUN ls -la /tmp
RUN mkdir /app/src/delaware_models
RUN cp -dpvR /tmp/foodex2PreditionDeployed/* /app/src/delaware_models
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN python -c "import nltk;nltk.download('stopwords')"
WORKDIR /app
COPY . /app
CMD [ "python", "app.py" ]
