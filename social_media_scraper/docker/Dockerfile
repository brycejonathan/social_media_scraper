# docker/Dockerfile

FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Install the package
RUN pip install .

# Expose port for API (if running Flask API)
EXPOSE 5000

# Command to run the CLI or API
# For CLI usage:
# ENTRYPOINT ["social-scraper"]
# For API usage:
CMD ["python", "-m", "api.api"]
