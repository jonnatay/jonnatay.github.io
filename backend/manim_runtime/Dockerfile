FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libcairo2-dev \
        libpango1.0-dev \
        pkg-config \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install sortedcontainers manim

RUN groupadd --system manim \
    && useradd --system --create-home --gid manim --shell /usr/sbin/nologin manim

COPY . /app
RUN chown -R manim:manim /app

WORKDIR /app
USER manim

CMD ["manim"]
