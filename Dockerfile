FROM python:3.7.2-slim

COPY ./requirements.txt /api/requirements.txt

WORKDIR /api

RUN  apt update 
RUN  apt install xfonts-75dpi xfonts-base gvfs colord glew-utils libvisual-0.4-plugins gstreamer1.0-tools opus-tools qt5-image-formats-plugins qtwayland5 qt5-qmltooling-plugins librsvg2-bin lm-sensors
RUN  wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb 
RUN  dpkg -i wkhtmltox_0.12.5-1.stretch_amd64.deb 
RUN  cp /usr/local/bin/wkhtmltopdf /usr/bin/ 
RUN  cp /usr/local/bin/wkhtmltoimage /usr/bin/

RUN pip3 install -r requirements.txt

COPY . /api

EXPOSE 5000

ENTRYPOINT ["uvicorn", "app.server:app", "--port", "5000"]
