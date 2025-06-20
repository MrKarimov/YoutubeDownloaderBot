FROM python:3.11-slim

# Tizim paketlarini o‘rnatamiz (ffmpeg kerak)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean

# yt-dlp va boshqa kutubxonalarni yangilaymiz
RUN pip install --no-cache-dir --upgrade pip yt-dlp

# Ishchi katalog
WORKDIR /app

# requirements.txt ni nusxalaymiz va o‘rnatamiz
COPY requirements.txt ./
COPY cookies.txt /app/cookies.txt
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini nusxalaymiz
COPY . .

# Botni ishga tushiramiz
CMD ["python", "main.py"]
