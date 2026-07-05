FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip

COPY pyproject.toml README.md ./
COPY src ./src
COPY backend ./backend
COPY frontend ./frontend
COPY knowledge ./knowledge
COPY database ./database

RUN pip install .

EXPOSE 8000 8501

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
