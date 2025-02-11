# Use a smaller base image
FROM python:3.12-alpine AS base

# Set up the working directory
WORKDIR /app

# Install dependencies in a separate stage to leverage caching
FROM base AS builder
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
FROM base AS final
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .

# Install Nginx and Supervisor
RUN apk add --no-cache nginx supervisor

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the Supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the ports for Nginx and Uvicorn
EXPOSE 80 8000

# Start Supervisor to manage both Nginx and Uvicorn
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]