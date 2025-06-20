import os
import logging
import urllib.request
from pytubefix import YouTube
from birlashtirish import merge_video_audio

# ✅ Log sozlamasi
logger = logging.getLogger(__name__)

# ✅ Global User-Agent (403 xatolikdan saqlaydi)
opener = urllib.request.build_opener()
opener.addheaders = [
    (
        "User-Agent",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
]
urllib.request.install_opener(opener)

# 📁 Yuklab olingan fayllar saqlanadigan papka
os.makedirs("downloads", exist_ok=True)


def get_resolutions(link):
    try:
        yt = YouTube(link)
        streams = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
        resolutions = set()

        for s in streams:
            if s.resolution:
                resolutions.add(s.resolution)

        return sorted(resolutions, reverse=True)
    except Exception as e:
        logger.error(f"Error in get_resolutions(): {e}", exc_info=True)
        print("Error:", e)
        return []


def download_video(link, resolution):
    try:
        yt = YouTube(link)
        
        # progressive (video + audio) ni qidirish
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()

        if stream:
            file_path = stream.download(output_path="downloads", filename=f"{yt.video_id}_{resolution}.mp4")
            return file_path

        # Aks holda video + audio alohida yuklab, birlashtirish kerak
        video = yt.streams.filter(adaptive=True, file_extension='mp4', resolution=resolution).first()
        audio = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        if video and audio:
            return merge_video_audio(video, audio, yt.video_id, resolution)

        return None
    except Exception as e:
        logger.error(f"Download Error in download_video(): {e}", exc_info=True)
        print("Download Error:", e)
        return None
