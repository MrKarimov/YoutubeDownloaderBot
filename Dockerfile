FROM python:3.11-slim

# ffmpeg va kerakli tizim paketlarini o‘rnatamiz
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# ishchi papkaga o‘tamiz
WORKDIR /app

# requirements.txt va kod fayllarini nusxalaymiz
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# botni ishga tushiramiz
CMD ["python", "main.py"]
