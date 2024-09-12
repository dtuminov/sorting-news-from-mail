FROM python:3.9.20-slim-bookworm

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "dags/ml-pipeline.py"]