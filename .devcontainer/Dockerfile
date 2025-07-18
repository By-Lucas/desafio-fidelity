FROM python:3.11-slim

# Instalações básicas
RUN apt-get update && apt-get install -y \
    curl wget gnupg unzip \
    fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxrandr2 xdg-utils lsb-release \
    libgbm-dev libxshmfence-dev libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Instala Microsoft Edge
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg && \
    install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/ && \
    sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list' && \
    apt-get update && apt-get install -y microsoft-edge-stable

# Instala msedgedriver compatível
RUN EDGE_VERSION=$(microsoft-edge --version | awk '{print $3}') && \
    DRIVER_URL="https://msedgedriver.azureedge.net/${EDGE_VERSION}/edgedriver_linux64.zip" && \
    wget -O /tmp/edgedriver.zip $DRIVER_URL && \
    unzip /tmp/edgedriver.zip -d /usr/bin && \
    chmod +x /usr/bin/msedgedriver && \
    rm /tmp/edgedriver.zip

# Define o display virtual se necessário
ENV DISPLAY=:99

# Instala dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /workspace
