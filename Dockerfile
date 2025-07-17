ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.19
FROM $BUILD_FROM

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-wheel \
    py3-setuptools \
    sqlite \
    gcc \
    musl-dev \
    python3-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev

# Upgrade pip and install Python packages
RUN pip3 install --upgrade pip setuptools wheel

# Install Python packages one by one to better handle errors
RUN pip3 install --no-cache-dir flask==2.3.3
RUN pip3 install --no-cache-dir flask-sqlalchemy==3.0.5
RUN pip3 install --no-cache-dir werkzeug==2.3.7
RUN pip3 install --no-cache-dir pillow==10.0.1
RUN pip3 install --no-cache-dir pandas==2.1.1
RUN pip3 install --no-cache-dir openpyxl==3.1.2

# Copy application files
COPY app/ /app/
COPY run.sh /
RUN chmod a+x /run.sh

# Create data directory
RUN mkdir -p /data

WORKDIR /app
EXPOSE 8080

CMD ["/run.sh"]