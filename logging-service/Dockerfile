FROM java:8-jdk-alpine

COPY /src /src/
COPY /out /out/
COPY /libs /libs/

RUN javac -d /out -cp /libs/*.jar /src/Program.java
CMD java ..

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "-u", "logging-service.py"]