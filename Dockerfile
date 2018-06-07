from python:3

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install .

ENV MONGO_HOST=localhost:27017
ENV PYTHONPATH=$PYTHONPATH:/app

CMD [ 'battleground_start', '--use_db', '--dynamic', '--registered_games=registered_games_production.json', '-d']
