FROM python:3.10.0-slim-bullseye

WORKDIR /app

# Install dependencies
RUN python -m ensurepip --upgrade
COPY requirements.txt .
RUN pip install -r requirements.txt

# Switch to non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Copy application files
COPY . .

# Run application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
