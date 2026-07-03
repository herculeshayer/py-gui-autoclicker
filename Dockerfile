FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Use Ubuntu's own python3 + python3-tk so the tkinter C extension always
# matches the interpreter ABI (mixing a distro's python3-tk with a
# separately-built python, e.g. the official python:3.x-slim image, breaks
# the tkinter import).
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-tk \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir pyautogui

WORKDIR /app
COPY main.py ./

CMD ["python3", "main.py"]
