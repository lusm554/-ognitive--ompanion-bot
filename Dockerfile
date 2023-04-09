FROM python:3.10-slim-buster
WORKDIR /bot
RUN apt-get update && apt-get install -y git
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "-u", "bot/main.py"] # using flag -u for unbuffered, to see python output
