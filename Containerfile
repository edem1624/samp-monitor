FROM alpine:3.19

LABEL org.opencontainers.image.source=https://github.com/edem1624/samp-monitor

ENV PYTHONUNBUFFERED=1

# Install Python
RUN apk add --update --no-cache py3-pip

WORKDIR /usr/src/app

# Install pip packages
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "/usr/src/app/app.py" ]
