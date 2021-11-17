ARG VENV_PATH=/opt/venv


FROM python:3.10.0-slim-bullseye as base
WORKDIR /app

# Set up venv
ARG VENV_PATH
RUN python3 -m venv "$VENV_PATH"
ENV PATH="${VENV_PATH}/bin:${PATH}"

# Install dependencies
RUN python -m ensurepip --upgrade
COPY requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.10.0-slim-bullseye as dev
WORKDIR /app

# Install dev dependencies and tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    git-all \
    less \
    openssh-client
RUN python -m ensurepip --upgrade
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# Copy all other files
COPY . .


FROM python:3.10.0-slim-bullseye as runtime

# Switch to non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Copy dependencies
ARG VENV_PATH
COPY --from=base "$VENV_PATH" "$VENV_PATH"
ENV PATH="${VENV_PATH}/bin:${PATH}"

# Copy application
COPY app.py .

# Set runtime variables
ARG VERSION
ARG COMMIT_SHA
ENV VERSION=$VERSION
ENV COMMIT_SHA=$COMMIT_SHA

# Run application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
