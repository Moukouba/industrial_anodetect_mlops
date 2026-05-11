# Multi-stage Dockerfile for FastAPI

# Build stage: Installs dependencies
FROM python:3.11.2-slim AS builder

# Set working directory inside the container
WORKDIR /app

# Install build dependencies (e.g., for some pip packages)
# Corrected 'install' to 'apt-get install'
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt from the project root (assuming Dockerfile is in 'docker/')
COPY requirements/requirements.txt .

# Install Python dependencies using --user to install into /root/.local
# Corrected '--uder' to '--user'
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage: Creates a lean image for running the application
FROM python:3.11.2-slim

# Create a non-root user for enhanced security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from the builder stage's /root/.local
# These are installed with --user in the builder, so they are in /root/.local
# We copy them to /home/appuser/.local in the production stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy the entire 'src' directory to '/app/src' to preserve the package structure
COPY src ./src

# Create the 'distributions' directory for model files
RUN mkdir -p distributions

# Copy model files from the project root's 'distributions/' folder
# Corrected paths to reflect they are in 'distributions/'
COPY distributions/padim_model.onnx ./distributions/
COPY distributions/padim_model.onnx.data ./distributions/
#COPY distributions/model_padim.pt ./distributions/
# Assuming model_info.json is also needed
COPY distributions/model_info.json ./distributions/

# Change ownership of the /app directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Set Matplotlib configuration directory to a writable path
ENV MPLCONFIGDIR=/tmp

# Add the user's local bin directory to PATH
# This ensures executables like 'uvicorn' and 'python' from --user installs are found
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose the port the FastAPI application will listen on
EXPOSE 8000

# Health check: Checks if the /health endpoint is reachable
# Using explicit python path and ensuring requests is available (from requirements.txt)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["/home/appuser/.local/bin/python", "-c", "import requests; requests.get('http://localhost:8000/health').raise_for_status()"] || exit 1

# Command to run the FastAPI application using uvicorn
# Corrected 'uvcorn' to 'uvicorn' and used explicit path
# The app is 'src.fastapi_app:app' because fastapi_app.py is copied directly to /app
CMD ["/home/appuser/.local/bin/uvicorn", "src.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
