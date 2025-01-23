# BASE IMAGE
FROM python:3.13-slim

# SET WORKING DIRECTORY
WORKDIR /app

# COPY APPLICATION CODE
COPY . /app

# INSTALL SYSTEM DEPENDENCIES
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# COPY REQUIREMENTS FIRST FOR CACHING
COPY requirements.txt .

# INSTALL PYTHON DEPENDENCIES
RUN pip install --no-cache-dir -r requirements.txt

# INSTALL AWS CLI
RUN pip install --no-cache-dir awscli


# ENVIRONMENT VARIABLES
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# EXPOSE PORT
EXPOSE 8080

# START COMMAND
CMD ["python3", "app.py"]


# # Use slim Bookworm variant for smaller size and updated packages
# FROM python:3.13-slim-bookworm

# WORKDIR /app

# # Install system dependencies first (combine apt operations in single layer)
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     build-essential \
#     libgomp1 \
#     && pip install --no-cache-dir awscli \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements first for better layer caching
# COPY requirements.txt .

# # Install Python dependencies with no caching
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy application code after dependency installation
# COPY . .

# CMD ["uvicorn", "app:app"]
# # CMD ["python3","app.py"]