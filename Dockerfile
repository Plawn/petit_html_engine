FROM python:3.7.2-slim

COPY ./requirements.txt /api/requirements.txt

WORKDIR /api

RUN apt-get install wkhtmltopdf

RUN pip3 install -r requirements.txt

COPY . /api

EXPOSE 5000

ENTRYPOINT ["uvicorn", "app.server:app", "--port", "5000"]
