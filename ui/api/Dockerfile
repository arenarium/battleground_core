FROM alpine:3.6

EXPOSE 3031
#VOLUME /usr/src/app/public
WORKDIR /app

RUN apk add --no-cache \
        uwsgi \
        uwsgi-python3 \
        python3

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
               "--plugins", "python3", \
               "--protocol", "uwsgi", \
               "--wsgi-file", "app.py",\
               "--callable", "app"]
