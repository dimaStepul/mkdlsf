FROM python:3.9-slim as builder

WORKDIR /app

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.9-slim

WORKDIR /app

RUN useradd -m myuser

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

COPY --chown=myuser:myuser . .

RUN chown -R myuser:myuser /app

USER myuser

CMD ["python3", "http_bypassing.py"]