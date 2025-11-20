# Multi-stage Dockerfile for Flask application
# Stage 1: Dependency installation and build
FROM python:3.9-slim AS dependency_builder

# Set working directory for build stage
WORKDIR /build

# Copy dependency file and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime image with minimal footprint
FROM python:3.9-slim AS runtime

# Set working directory for application
WORKDIR /app

# Copy installed Python packages from builder stage
COPY --from=dependency_builder /root/.local /root/.local

# Copy application source code
COPY app.py .

# Update PATH to include user-installed packages
ENV PATH=/root/.local/bin:$PATH

# Expose Flask default port
EXPOSE 5000

# Run Flask application
CMD ["python", "app.py"]
