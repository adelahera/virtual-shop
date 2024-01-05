FROM python:3.11-alpine

RUN pip install --upgrade pip

COPY ./e-commerce /app

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
