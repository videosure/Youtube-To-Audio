# Youtube-To-Audio
A simple Python utility to download YouTube videos as MP3 or WAV audio files using yt-dlp and a bundled FFmpeg binary via imageio-ffmpeg.


# Prerequisites

Python 3.7 or higher

Windows (for the provided .bat), macOS or Linux will work for the Python script directly

Internet access to download from YouTube

Install Python dependencies: pip install yt-dlp imageio-ffmpeg

# Usage

From the command line
python youtube_to_audio.py <YOUTUBE_URL> [-f {mp3,wav}] [-o OUTPUT_DIR]

<YOUTUBE_URL>: One or more valid YouTube video URLs.

-f, --format: Output format, either mp3 (default) or wav.

-o, --output: Destination folder (default: downloads/).

Example: python youtube_to_audio.py https://www.youtube.com/watch?v=VIDEO_ID -f wav -o my_audios
