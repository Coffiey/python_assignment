FROM python:3.7-alpine
WORKDIR /code
COPY . .
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt
EXPOSE 5000
CMD flask run