FROM python:3.9.7
RUN apt-get update && apt-get install git -y
COPY . .
RUN pip3 install -U pip && pip3 install -r requirements.txt
CMD python3 -m Home
