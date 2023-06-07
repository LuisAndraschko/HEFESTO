FROM python:3.10-bullseye as python-base

RUN apt update && apt install -y \
    gcc \
    gfortran \
    python3 \
    python3-dev \
    wget \
    libpng-dev \
    bpfcc-tools \
    libbpfcc \
    libbpfcc-dev 

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

FROM python:3.10-bullseye

ENV PYTHONUNBUFFERED True
ENV PORT 8080

WORKDIR /app

COPY --from=python-base /app /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache

CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 run:app
