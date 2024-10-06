FROM python:3.11.9

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get -y install tesseract-ocr && pip install -r requirements.txt

EXPOSE 3001

CMD [ "python", "./src/server.py" ]

