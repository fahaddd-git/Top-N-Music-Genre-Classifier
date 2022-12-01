FROM python:3.10-slim

# install c-libraries required for librosa's soundfile dependency
RUN apt-get update && apt-get install -y libsndfile-dev ffmpeg

# avoid writing .pyc since docker will create a new container each time anyway
ENV PYTHONDONTWRITEBYTECODE 1

ARG POETRY_VERSION=1.2.0
ARG APP_DIR=/app
ARG UTILTIES_DIR=/utilities

# Install poetry with some sane options for docker: (1) install only required dependencies;
# (2) don't cache anything outside the container's build environment; (3) use the system, i.e.,
# container, interpreter's environment instead of creating a virtual environment
RUN pip3 install poetry==${POETRY_VERSION}
RUN poetry config cache-dir ${APP_DIR}/.cache
RUN poetry config virtualenvs.create false

# copy the utilities package
WORKDIR $UTILTIES_DIR
COPY --from=utilities utilities /utilities

# install the prediction api
WORKDIR $APP_DIR
COPY pyproject.toml poetry.lock $APP_DIR
COPY . $APP_DIR
RUN poetry install --without dev -n --no-ansi

# Heroku doesn't permit docker containers to run as root, so create and run as non-root user:
# https://devcenter.heroku.com/articles/container-registry-and-runtime#run-the-image-as-a-non-root-user
RUN useradd -m api-user
USER api-user

# repeat poetry config for the api-user
RUN poetry config cache-dir ${APP_DIR}/.cache
RUN poetry config virtualenvs.create false

CMD ["poetry", "run", "start"]
