FROM alpine

# the editable install be handled by poetry; we just need to copy the source code
WORKDIR /utilities

COPY pyproject.toml poetry.lock $APP_DIR
COPY utilities ./utilities
