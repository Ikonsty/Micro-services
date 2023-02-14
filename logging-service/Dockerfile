FROM python:3.8

RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "-u", "logging-service.py"]