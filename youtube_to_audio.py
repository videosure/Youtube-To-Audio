import argparse
import os
import sys

from yt_dlp import YoutubeDL
from imageio_ffmpeg import get_ffmpeg_exe

# python youtube_to_audio.py https://www.youtube.com/watch?v=VIDEO_ID
# cd the folder that the scripts is in

def download_audio(url, output_format, output_path):
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Get a bundled FFmpeg executable
    ffmpeg_path = get_ffmpeg_exe()

    # Prepare yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': ffmpeg_path,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Download complete: {url} -> {output_format} in {output_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos as MP3 or WAV audio files.")
    parser.add_argument(
        'urls',
        nargs='+',
        help='One or more YouTube video URLs to download.'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['mp3', 'wav'],
        default='mp3',
        help='Output audio format (mp3 or wav). Default: mp3.'
    )
    parser.add_argument(
        '-o', '--output',
        default='downloads',
        help='Output directory. Default: ./downloads'
    )

    args = parser.parse_args()

    for url in args.urls:
        download_audio(url, args.format, args.output)


if __name__ == '__main__':
    main()