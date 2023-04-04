FROM python:3

WORKDIR /ChildFeedBot

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

