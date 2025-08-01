import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from yt_dlp import YoutubeDL
from imageio_ffmpeg import get_ffmpeg_exe


def download_audio(url, output_format, output_path, log_callback):
    os.makedirs(output_path, exist_ok=True)
    ffmpeg_path = get_ffmpeg_exe()
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': ffmpeg_path,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    def run():
        try:
            with YoutubeDL(ydl_opts) as ydl:
                log_callback(f"Starting download: {url}\n")
                ydl.download([url])
            log_callback(f"Download complete: {url} -> {output_format} in {output_path}\n")
        except Exception as e:
            log_callback(f"Error downloading {url}: {e}\n")

    thread = threading.Thread(target=run)
    thread.start()


def browse_folder(entry_widget):
    directory = filedialog.askdirectory()
    if directory:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, directory)


def on_download():
    url = url_entry.get().strip()
    fmt = format_var.get()
    out = output_entry.get().strip() or 'downloads'
    if not url:
        messagebox.showwarning("Input Error", "Please enter a YouTube URL.")
        return
    log_text.configure(state=tk.NORMAL)
    log_text.delete('1.0', tk.END)
    log_text.configure(state=tk.DISABLED)
    download_audio(url, fmt, out, log_callback=append_log)


def append_log(message):
    log_text.configure(state=tk.NORMAL)
    log_text.insert(tk.END, message)
    log_text.see(tk.END)
    log_text.configure(state=tk.DISABLED)


# GUI setup
root = tk.Tk()
root.title("YouTube to Audio Downloader")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

# URL input
tk.Label(frame, text="YouTube URL:").grid(row=0, column=0, sticky=tk.W)
url_entry = tk.Entry(frame, width=50)
url_entry.grid(row=0, column=1, columnspan=2, pady=5)

# Format selection
format_var = tk.StringVar(value='mp3')
tk.Label(frame, text="Format:").grid(row=1, column=0, sticky=tk.W)
mp3_radio = tk.Radiobutton(frame, text="MP3", variable=format_var, value='mp3')
mp3_radio.grid(row=1, column=1, sticky=tk.W)
wav_radio = tk.Radiobutton(frame, text="WAV", variable=format_var, value='wav')
wav_radio.grid(row=1, column=2, sticky=tk.W)

# Output folder
tk.Label(frame, text="Output Folder:").grid(row=2, column=0, sticky=tk.W)
output_entry = tk.Entry(frame, width=40)
output_entry.insert(0, os.path.join(os.getcwd(), 'downloads'))
output_entry.grid(row=2, column=1, pady=5)
browse_btn = tk.Button(frame, text="Browse...", command=lambda: browse_folder(output_entry))
browse_btn.grid(row=2, column=2, padx=5)

# Download button
download_btn = tk.Button(frame, text="Download", width=20, command=on_download)
download_btn.grid(row=3, column=0, columnspan=3, pady=10)

# Log output
log_text = tk.Text(frame, height=10, state=tk.DISABLED)
log_text.grid(row=4, column=0, columnspan=3, pady=5)

root.mainloop()
