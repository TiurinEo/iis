FROM python:3.11-slim

COPY . /ml_service

VOLUME ["/models"]

WORKDIR /ml_service

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t ml-prediction-service:1 .
# docker run -d -p 8000:8000 -v $(pwd)/../models:/models ml-prediction-service:1