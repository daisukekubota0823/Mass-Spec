# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for Python and R
RUN apt-get update && apt-get install -y \
    r-base \
    libcurl4-openssl-dev \
    libssl-dev \
    && apt-get clean

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Ensure R packages are installed
RUN Rscript -e "install.packages('methods', repos='http://cran.us.r-project.org')"

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
