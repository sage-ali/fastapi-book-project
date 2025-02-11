FROM python:3.12-slim

# Install Nginx and Supervisor
RUN apt-get update && apt-get install -y nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/sites-available/default

# Copy the Supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the ports for Nginx and Uvicorn
EXPOSE 80 8000

# Start Supervisor to manage both Nginx and Uvicorn
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]