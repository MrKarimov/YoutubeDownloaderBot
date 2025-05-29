import os

def merge_video_audio(video_stream, audio_stream, video_id, resolution):
    try:
        video_path = f"{video_id}_video.mp4"
        audio_path = f"{video_id}_audio.mp4"
        output_path = f"{video_id}_{resolution}_merged.mp4"

        video_stream.download(filename=video_path)
        audio_stream.download(filename=audio_path)

        # ffmpeg birlashtirish
        os.system(f"ffmpeg -y -i {video_path} -i {audio_path} -c:v copy -c:a aac {output_path}")

        # vaqtinchalik fayllarni o'chirish
        os.remove(video_path)
        os.remove(audio_path)

        return output_path

    except Exception as e:
        print("Merging error:", e)
        return None
