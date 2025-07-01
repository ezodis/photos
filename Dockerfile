FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install Flask

RUN mkdir -p /app/media /app/static

CMD ["python", "photo_viewer.py"]
