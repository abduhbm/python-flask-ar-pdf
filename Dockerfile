# Pull a pre-built alpine docker image with nginx and python3 installed
FROM python:3.7-alpine

EXPOSE 5000

RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN apk add --update tini

COPY . /app
COPY requirements.txt /app
WORKDIR /app

RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

ENTRYPOINT ["/sbin/tini", "--"]

CMD ["gunicorn", "-w 3", "-b :5000", "app:app"]