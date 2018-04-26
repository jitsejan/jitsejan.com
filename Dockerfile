FROM python:3
RUN apt-get update -y
RUN apt-get install node-less -y
RUN mkdir /code
WORKDIR /code
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
