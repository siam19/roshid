FROM python:3.11.9

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get -y install tesseract-ocr && pip install -r requirements.txt

EXPOSE 4000

CMD [ "python", "./src/server.py" ]

