from pytubefix import YouTube
from birlashtirish import merge_video_audio

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
        print("Error:", e)
        return []

def download_video(link, resolution):
    try:
        yt = YouTube(link)
        
        # progressive (video + audio) ni qidirish
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()

        if stream:
            file_path = stream.download(filename=f"{yt.video_id}_{resolution}.mp4")
            return file_path

        # Aks holda video + audio alohida yuklab, birlashtirish kerak
        video = yt.streams.filter(adaptive=True, file_extension='mp4', resolution=resolution).first()
        audio = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        if video and audio:
            return merge_video_audio(video, audio, yt.video_id, resolution)

        return None
    except Exception as e:
        print("Download Error:", e)
        return None
