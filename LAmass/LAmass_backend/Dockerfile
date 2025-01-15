# Base Python image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    r-base \
    && apt-get clean

# Install R packages
RUN R -e "install.packages('jsonlite')"

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
