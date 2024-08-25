FROM python:3.12-slim AS builder

COPY ./app/requirements.txt requirements.txt
COPY ./app/requirements-dev.txt requirements-dev.txt

RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

ARG ENV
RUN if [ "$ENV" = "test" ]; then \
    pip install --user --no-cache-dir -r requirements-dev.txt; \
    fi;

FROM python:3.12-slim AS production

# Keeps python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering fro easier container logging
ENV PYTHONBUFFERED=1

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

WORKDIR /code

COPY ./app /code/app
