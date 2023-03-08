FROM python:alpine3.8

WORKDIR /flask-app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./

CMD ["python","app.py"]