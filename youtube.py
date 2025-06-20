import os
import logging
from yt_dlp import YoutubeDL

# Log sozlamasi
logger = logging.getLogger(__name__)

# Yuklab olingan fayllar uchun papka
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_resolutions(link):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'noplaylist': True,
            'cookies': './cookies.txt',
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            formats = info.get("formats", [])

            resolutions = set()
            for f in formats:
                if f.get("height") and f.get("vcodec") != "none":
                    resolutions.add(f"{f['height']}p")

            return sorted(resolutions, reverse=True)

    except Exception as e:
        logger.error(f"❌ Error in get_resolutions(): {e}", exc_info=True)
        return []

def download_video(link, resolution):
    try:
        height = resolution.replace("p", "")
        ydl_opts = {
            'format': f'bestvideo[height={height}]+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(DOWNLOAD_DIR, f'%(title)s_{resolution}.%(ext)s'),
            'noplaylist': True,
            'cookies': './cookies.txt',
            'quiet': True,
            'user_agent': (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp4")

            if os.path.exists(filename):
                return filename
            else:
                logger.warning("❌ File expected but not found after download.")
                return None

    except Exception as e:
        logger.error(f"❌ Download Error in download_video(): {e}", exc_info=True)
        return None
