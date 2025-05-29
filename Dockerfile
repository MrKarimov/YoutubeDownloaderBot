FROM python:3.11-slim

# tizim paketlarini o'rnatamiz, jumladan ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

WORKDIR /app

# pipenv o'rnatish
RUN pip install --no-cache-dir pipenv

# loyiha fayllarini ko'chiramiz
COPY Pipfile Pipfile.lock /app/

# dependencies ni pipenv bilan o'rnatamiz
RUN pipenv install --deploy --ignore-pipfile

# qolgan fayllarni nusxalaymiz
COPY . .

# konteynerda botni pipenv muhitida ishga tushiramiz
CMD ["pipenv", "run", "python", "main.py"]
