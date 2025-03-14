#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please create it from .env.example"
    echo "cp .env.example .env"
    exit 1
fi

# Build and run the Docker container
echo "Building and starting the OOF scheduler container..."
docker compose up -d --build

echo "Container started. You can check logs with:"
echo "docker-compose logs -f" 