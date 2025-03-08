FROM python:3.12-slim AS python

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PATH="$PATH:$POETRY_HOME/bin"

FROM python AS builder

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && apt-get install -y libpq-dev \
    && apt-get install -y build-essential \
    && apt-get -y install --no-install-recommends postgresql-client

WORKDIR /opt/pysetup
# COPY pyproject.toml poetry.lock .mise.toml ./



COPY ./gig_tracker/ ./gig_tracker
RUN cd gig_tracker
RUN POETRY_VERSION=$(grep -h poetry .mise.toml | awk -F"'" '{print $2}') && \
    curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION
RUN poetry install -n --without dev

FROM python AS runtime

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/python3120/lib
ENV POETRY_HOME="/opt/poetry"

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder /opt/pysetup /opt/pysetup

ENV PATH="$PATH:$POETRY_HOME/bin"
WORKDIR /opt/pysetup

EXPOSE 80

# ENTRYPOINT ["poetry", "run", "uvicorn", "app:app", "--reload", "--host=0.0.0.0", "--port=80"]