from python:3

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .


ENV MONGO_HOST=localhost:27017
ENV PYTHONPATH=$PYTHONPATH:/app

CMD [ "python", "start.py", "--dynamic", "-d"]
