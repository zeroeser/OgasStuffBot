FROM python:3.13-slim-bookworm

WORKDIR /usr/app/src

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install 
# - python3-pip for pip 
# - curl for healthcheck
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends curl python3-pip\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN  pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt

COPY /src /usr/app/src

ENTRYPOINT ["python" , "main.py"]
