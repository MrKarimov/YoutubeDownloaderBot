# 🎬 YouTube Downloader Telegram Bot

This is a Telegram bot built with Python that allows users to download YouTube videos by simply sending a video link. It supports resolution selection and handles both progressive and adaptive YouTube streams. If the video and audio are separate, the bot uses `ffmpeg` to merge them before sending.

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **Aiogram 3** – Telegram bot framework (async)
- **aiosqlite** – Asynchronous SQLite database
- **pytube** – YouTube video parsing and downloading
- **ffmpeg** – For merging audio and video streams
- **dotenv** – Environment variable management
- **SQLite** – Local database to store users

---

## 🚀 Getting Started

### 1. Clone the repository


git clone https://github.com/yourusername/yourbot.git
cd yourbot
## 2. Create a virtual environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
## 3. Install dependencies
bash
pip install -r requirements.txt
## 4. Create a .env file
env
BOT_TOKEN=your_telegram_bot_token
ADMIN=your_telegram_user_id
##  5. Install ffmpeg
Linux (Ubuntu/Debian)
sudo apt install ffmpeg
Windows
Download and install from: https://ffmpeg.org/download.html

🧰 Features
📥 Download videos from YouTube by link

🎞 Choose video quality from available resolutions

🔊 Merge video and audio streams if separated (adaptive)

👤 Store user data in SQLite

👮 Admin panel:

👥 View registered users

📠 Export users to CSV

📢 Send broadcast messages (text or image)

📁 Project Structure
.
├── main.py               # Bot launcher and dispatcher setup
├── admin.py              # Admin commands (CSV, broadcast, etc.)
├── handlers.py           # User commands (/start, etc.)
├── youtube.py            # Video parsing and download logic
├── birlashtirish.py      # Merges audio and video using ffmpeg
├── database/
│   └── database.py       # SQLite functions: add, query users
├── requirements.txt      # Project dependencies
├── .env                  # Bot token and admin ID (excluded from Git)
└── .gitignore            # Ignored files and folders

## 🧠 How birlashtirish.py Works
Some YouTube videos are streamed as separate audio and video tracks (adaptive format). This script uses ffmpeg to merge them before sending to the user:

python
import subprocess

def merge_audio_video(video_path, audio_path, output_path):
    command = [
        "ffmpeg",
        "-i", video_path,
        "-i", audio_path,
        "-c", "copy",
        output_path
    ]
    subprocess.run(command, check=True)
The merged file is then uploaded to Telegram using FSInputFile.

## 📊 Admin Panel Commands
Accessible only to the admin defined in .env:

/admin – Open admin panel

👥 Users – View all registered users

📠 Create CSV – Export users as CSV file

📢 Send Ads – Broadcast a message (supports text or photo)

🛡️ Security Notes
Your .env file contains sensitive data — make sure it's listed in .gitignore.

Don't commit your database or virtual environment folders.



## 🙋 Author
Islom Karimov


