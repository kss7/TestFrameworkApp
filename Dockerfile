#Dockerfile
#docker build -t mysmartapp .
#docker run -d -p 5000:5000 mysmartapp

FROM python:3.10-slim-buster
ADD . /pytestapp
WORKDIR /pytestapp
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./run.py" ]