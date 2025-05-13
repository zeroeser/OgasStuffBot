FROM python:3.10.4-slim-buster

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on
ENV PYTHONPATH="$PYTHONPATH:/mnt"
ENV GK_VERSION v0.32.0
ENV POETRY_VERSION=1.2.2
ENV TZ=Europe/Moscow
ENV FF_VER 108.0
ENV FF_DIR /usr/bin

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ARG USER=${UID:-1001}

WORKDIR /opt
COPY --chown=$USER poetry.lock pyproject.toml /opt/

RUN pip3 install "poetry==$POETRY_VERSION" "poetry-core==1.3.2" && poetry config virtualenvs.create false && \
   poetry config installer.parallel false

RUN poetry install --no-root --no-interaction --no-ansi -vvv


COPY --chown=$USER . /opt
EXPOSE 8080
