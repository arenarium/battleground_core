from python:3

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .


ENV COUCHDB_HOST=http://localhost:5984
ENV PYTHONPATH=$PYTHONPATH:/app

CMD [ "python", "start.py", "--dynamic", "-d"]
