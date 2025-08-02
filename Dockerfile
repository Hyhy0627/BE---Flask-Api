FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY src/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create instance directory for SQLite database
RUN mkdir -p instance

# Copy application code explicitly
COPY src/app.py .
COPY src/api/ ./api/
COPY src/domain/ ./domain/
COPY src/infrastructure/ ./infrastructure/
COPY src/services/ ./services/
COPY src/scripts/ ./scripts/
COPY src/create_app.py .
COPY src/app_logging.py .
COPY src/config.py .
COPY src/cors.py .
COPY src/error_handler.py .
COPY src/dependency_container.py .
COPY src/swagger_config.json .
COPY src/show_routes.py .
COPY src/manage.py .
COPY src/entrypoint.sh .

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 5000

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Command to run the application
CMD ["/app/entrypoint.sh"]
