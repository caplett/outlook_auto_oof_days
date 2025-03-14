FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Add healthcheck
HEALTHCHECK --interval=1h --timeout=30s --start-period=30s --retries=3 \
  CMD python -c "import os; exit(0 if os.path.exists('/app/logs') else 1)"

# Run the script
CMD ["python", "-u", "set_oof.py"] 