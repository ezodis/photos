FROM python:3.9 AS builder

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Final image
FROM python:3.9
WORKDIR /app

# Copy dependencies from the builder stage
COPY --from=builder /app /app
COPY . /app

# Explicitly install Flask to ensure it is available
RUN pip install Flask

# Check if Flask is installed correctly
RUN pip show Flask

# Create directories
RUN mkdir -p /app/media /app/static

CMD ["python", "photo_viewer.py"]
