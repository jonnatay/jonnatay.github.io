FROM python:3.11-slim

# Install system dependencies
RUN apt-get update
RUN apt-get install -y libcairo2-dev
RUN apt-get install -y libpango1.0-dev
RUN apt-get install -y pkg-config
RUN apt-get install -y build-essential
RUN apt-get install -y python3-dev
RUN rm -rf /var/lib/apt/lists/*

# Upgrade pip (optional but helps)
RUN pip install --upgrade pip
RUN pip install sortedcontainers
# Install manim
RUN pip install manim

COPY . /app

WORKDIR /app

CMD ["manim"]