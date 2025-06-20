import os
import logging
from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)
os.makedirs("downloads", exist_ok=True)

def get_resolutions(link):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'noplaylist': True,
            'cookies': 'cookies1.txt',
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
        output_path = f"downloads/%(title)s_{resolution}.mp4"

        ydl_opts = {
            'format': f'bestvideo[height={height}]+bestaudio/best[height={height}]',
            'merge_output_format': 'mp4',
            'outtmpl': output_path,
            'noplaylist': True,
            'quiet': True,
            'cookies': 'cookies1.txt',
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
            return None

    except Exception as e:
        logger.error(f"❌ Download Error in download_video(): {e}", exc_info=True)
        return None
