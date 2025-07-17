#!/usr/bin/with-contenv bashio

# Get configuration
ADMIN_USERNAME=$(bashio::config 'admin_username')
ADMIN_PASSWORD=$(bashio::config 'admin_password')
DATABASE_PATH=$(bashio::config 'database_path')
MAX_FILE_SIZE=$(bashio::config 'max_file_size')

# Export environment variables
export ADMIN_USERNAME="$ADMIN_USERNAME"
export ADMIN_PASSWORD="$ADMIN_PASSWORD"
export DATABASE_PATH="$DATABASE_PATH"
export MAX_FILE_SIZE="$MAX_FILE_SIZE"

bashio::log.info "Starting Visitor Management System..."
bashio::log.info "Admin username: $ADMIN_USERNAME"
bashio::log.info "Database path: $DATABASE_PATH"

# Start the Flask application
cd /app
python3 app.py