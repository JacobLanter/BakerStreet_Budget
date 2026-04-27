FROM python:3.11
WORKDIR /YNAB_Dashboard

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY backend/app ./src

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["python", "src/main.py"]