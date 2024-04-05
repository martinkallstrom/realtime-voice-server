FROM ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG USE_PERSISTENT_DATA
ENV PYTHONUNBUFFERED=1
ENV NODE_MAJOR=20

# Expose FastAPI port
ENV FAST_API_PORT=7860
EXPOSE 7860

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    python3.10 \
    python3-pip \
    python3-dev \
    git \
    ffmpeg \
    google-perftools \
    ca-certificates curl gnupg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /code

RUN mkdir -p /etc/apt/keyrings 
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list > /dev/null
RUN apt-get update && apt-get install nodejs -y

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user
# Switch to the "user" user
USER user
# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONPATH=$HOME/app \
    PYTHONUNBUFFERED=1

# Install Python dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Copy package.json and package-lock.json
COPY --chown=user frontend/package*.json frontend/
RUN cd frontend && npm install

# Copy frontend app and build
COPY --chown=user frontend/ frontend/
RUN cd frontend && npm run build

# Copy everything else
COPY --chown=user app/ app/
COPY --chown=user server.py server.py

ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4

CMD ["python3", "server.py", "--port", "$FAST_API_PORT"]
