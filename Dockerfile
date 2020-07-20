FROM python:slim

WORKDIR /usr/src/app

# We copy just the requirements.txt first to leverage Docker cache
COPY ["requirements.txt", "./"]
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import nltk;nltk.download('punkt')"

COPY . .

# Expose the Flask port
EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]