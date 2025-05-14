FROM python:3.11-slim

COPY requirements.txt /app/requirements.txt
RUN mkdir -p /app/src/logs && mkdir -p /app/src/data && pip install --no-cache-dir -r /app/requirements.txt

COPY src/ /app/src
ENV PYTHONPATH=/app/

WORKDIR /app/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]