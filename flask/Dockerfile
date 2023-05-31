# Dockerfile for flask
FROM python:3.10-bullseye as python-base

RUN apt update && apt install -y \
    gcc \
    gfortran \
    python3 \
    python3-dev \
    wget \
    libpng-dev

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10-bullseye

WORKDIR /app

COPY --from=python-base /app /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache
# Create a new user and group
RUN groupadd -r uwsgigroup && useradd -r -g uwsgigroup uwsgiuser

CMD ["uwsgi", "uwsgi.ini"]
