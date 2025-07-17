ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.19
FROM $BUILD_FROM

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    sqlite \
    gcc \
    musl-dev \
    python3-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev

# Create virtual environment to avoid conflicts
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip in virtual environment
RUN pip install --upgrade pip

# Install Python packages with specific versions that work well together
RUN pip install --no-cache-dir \
    flask==2.3.3 \
    flask-sqlalchemy==3.0.5 \
    werkzeug==2.3.7 \
    pillow==10.0.1 \
    pandas==2.1.1 \
    openpyxl==3.1.2

# Copy application files
COPY app/ /app/
COPY run.sh /
RUN chmod a+x /run.sh

# Create data directory
RUN mkdir -p /data

WORKDIR /app
EXPOSE 8080

CMD ["/run.sh"]