FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential curl git protobuf-compiler && \
    apt-get clean

COPY requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .

RUN mkdir -p generated && \
    python -m grpc_tools.protoc -I=proto --python_out=generated --grpc_python_out=generated proto/*.proto

FROM python:3.12-slim

RUN useradd -m -r appuser && mkdir /app && chown -R appuser /app

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "run:app"]
