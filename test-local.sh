#!/bin/bash

echo "Building and testing Visitor Management System locally..."

# Create data directory
mkdir -p data

# Build the Docker image
docker build -t ha-vms-test --build-arg BUILD_FROM=python:3.11-alpine .

# Run the container
docker run -d \
  --name ha-vms-test \
  -p 8080:8080 \
  -e ADMIN_USERNAME=admin \
  -e ADMIN_PASSWORD=changeme \
  -e DATABASE_PATH=/data/visitors.db \
  -e MAX_FILE_SIZE=10485760 \
  -v $(pwd)/data:/data \
  ha-vms-test

echo "Container started! Access the application at http://localhost:8080"
echo "Admin login: admin/changeme"
echo ""
echo "To stop the test container, run: docker stop ha-vms-test && docker rm ha-vms-test"