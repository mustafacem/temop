FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y  \
    curl  \
    ffmpeg  \
    libsm6  \
    libxext6

ENV POETRY_NO_INTERACTION=1 \
    POETRY_INSTALLER_PARALLEL=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_REQUESTS_TIMEOUT=100 \
    POETRY_CACHE_DIR=/tmp/poetry_cache
RUN pip install poetry

COPY ./poetry.lock ./
COPY ./pyproject.toml ./
RUN poetry install --no-interaction --no-cache --no-ansi
RUN pip install pyheif

COPY ./proposal_droid/ ./proposal_droid
COPY ./streamlit_main.py ./

CMD ["/bin/sh", "-c", "python -m streamlit run streamlit_main.py --server.port=8501 --server.address=0.0.0.0"]
