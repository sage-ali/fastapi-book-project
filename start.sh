#!/bin/bash

# Start Nginx
service nginx start

# Start Uvicorn
uvicorn main:app --host 127.0.0.1 --port 8000
