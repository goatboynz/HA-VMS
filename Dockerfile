ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python and required packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-pillow \
    sqlite \
    && pip3 install --no-cache-dir \
        flask \
        flask-sqlalchemy \
        werkzeug \
        pillow \
        pandas \
        openpyxl

# Copy application files
COPY app/ /app/
COPY run.sh /
RUN chmod a+x /run.sh

# Create data directory
RUN mkdir -p /data

WORKDIR /app
EXPOSE 8080

CMD ["/run.sh"]