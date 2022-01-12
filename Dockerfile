FROM python:3.8-slim

WORKDIR /usr/src/app

# We copy just the requirements.txt first to leverage Docker cache
COPY ["requirements-frozen.txt", "./"]
RUN pip install --no-cache-dir -r requirements-frozen.txt
RUN python -c "import nltk;nltk.download('wordnet');"
RUN python -c "import nltk;nltk.download('omw-1.4');"


COPY . .

# Expose the Flask port
EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
