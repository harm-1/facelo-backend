# syntax=docker/dockerfile:1

# ================================== BASE ===================================
FROM python:slim-buster AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /facelo/backend
EXPOSE 5000

RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  gcc \
  libffi-dev \
  && rm -rf /var/lib/apt/lists/*


# ================================= BUILDER =================================
FROM base AS builder

RUN pip install pipenv


# ================================= DEVELOPMENT ================================
FROM base AS development

RUN mkdir -p /home/harm/projects/Facelo
RUN ln -s /facelo/backend /home/harm/projects/Facelo

CMD [ "flask", "run", "--host", "0.0.0.0" ]


# ================================= PRODUCTION ================================
FROM base AS production

