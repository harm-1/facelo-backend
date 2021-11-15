# ================================== BUILDER ===================================
ARG PYTHON_IMAGE_VERSION=${PYTHON_IMAGE_VERSION}

FROM python:${PYTHON_IMAGE_VERSION} AS builder

RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  gcc \
  libffi-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv
WORKDIR /facelo/backend
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# ================================= PRODUCTION =================================
# zie cookiecutter

FROM builder AS production

# ================================= DEVELOPMENT ================================
FROM builder AS development

RUN mkdir -p /home/harm/projects/Facelo
RUN ln -s /facelo/backend /home/harm/projects/Facelo

RUN pipenv install --dev --system --deploy
EXPOSE 5000
CMD [ "flask", "run", "--host", "0.0.0.0" ]
