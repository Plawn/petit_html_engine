FROM python:3.8.6-slim

COPY ./requirements.txt /api/requirements.txt

WORKDIR /api

RUN  apt update && apt install wkhtmltopdf -y

RUN pip install -r requirements.txt

COPY . /api

EXPOSE 5000

ENTRYPOINT ["uvicorn", "app.server:app", "--port", "5000"]
