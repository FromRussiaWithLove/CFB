FROM python:3

WORKDIR /CFB

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

