# 1. Use an official Python runtime as a parent image
FROM python:3.13.5-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy requirements first for layer caching
COPY requirements.txt ./

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# (Optional) Install Git if using DVC inside container
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 5. Copy the rest of your code into the container
COPY . .

# 6. Expose the port the app runs on
EXPOSE 5000

# 7. Command to run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
