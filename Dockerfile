# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire project into the container
COPY . /app

# Expose the port that the app runs on
EXPOSE 8080

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# # Command to run the application with Gunicorn
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
# Command to run the application with Gunicorn
CMD ["gunicorn", "-w", "4", "-k", "gevent", "--timeout", "120", "-b", "0.0.0.0:8080", "app:app"]