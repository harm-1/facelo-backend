# syntax=docker/dockerfile:1

# ================================= BUILDER =================================
FROM python:slim-buster AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV WORKDIR=/facelo/backend
WORKDIR $WORKDIR

# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=${WORKDIR}/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

EXPOSE 5000

RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  pkg-config \
  gcc \
  libffi-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
COPY pyproject.toml .
RUN poetry install

# ================================= DEVELOPMENT ================================
FROM builder AS development

# I do this to be able to run pytest in emacs
RUN mkdir -p /home/harm/projects/facelo
RUN ln -s /facelo/backend /home/harm/projects/facelo

CMD [ "flask", "run", "--host", "0.0.0.0" ]


# ================================= PRODUCTION ================================
FROM base AS production
