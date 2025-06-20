FROM python:3.11-slim

# ishchi papkaga o‘tamiz
WORKDIR /app

# requirements.txt va kod fayllarini nusxalaymiz
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# botni ishga tushiramiz
CMD ["python", "main.py"]
