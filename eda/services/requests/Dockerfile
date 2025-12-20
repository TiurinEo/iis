FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY requests_sender.py .

CMD ["python", "-u", "requests_sender.py"]

# -----------------------------
# Build image:
# docker build -t ml-requests-service:1 .
#
# Run container:
# docker run --rm ml-requests-service:1
# -----------------------------
