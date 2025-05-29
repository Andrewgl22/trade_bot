# Use official Python base image
FROM python:3.11-slim

# Create a non-root user
RUN useradd -m botuser

# Set working directory (owned by root by default)
WORKDIR /app

# Copy requirements and install packages as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Change ownership so non-root user can access
RUN chown -R botuser:botuser /app

# Switch to non-root user *after everything is in place*
USER botuser

# Run the trading bot
# CMD ["python", "bot.py"]
