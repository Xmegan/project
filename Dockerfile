FROM python:3.10.4

WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app/
CMD chmod +x scripts/start_app.sh; scripts/start_app.sh