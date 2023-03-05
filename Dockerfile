FROM python:3.8

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "main.py"]





#FROM python:3.8
#
#RUN apt-get update && apt-get install -y redis-server
#WORKDIR /usr/src/app
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#COPY . .
#
#EXPOSE 6379
#
#CMD ["redis-server"]
#CMD ["python", "main.py"]

