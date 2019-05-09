# python-flask-ar-pdf
Simple example using Python/Flask to export Arabic PDFs from a dockerized microservice


#### To get the service running:
From the repo directory, build the container image and make it running:
```console
docker build -t flask-ar-pdf . && docker run -d -p 5000:5000 flask-ar-pdf
```

Access the Swagger UI page by visiting: http://localhost:5000/api

You can send a GET request to: http://localhost:5000/api/pdf/generate
