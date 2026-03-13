# YT Downloader Professional 🚀

A modern, fast, and robust YouTube Downloader built with Python, `customtkinter`, and `yt-dlp`.
Download video or audio from YouTube in the highest quality directly to your PC, while preserving the best audio bitrates and codecs!

## Features
- **Dark Mode UI**: Professional dark aesthetic using CustomTkinter.
- **Top Quality Video**: Automatically fetches the best visual feeds and merges them using `ffmpeg`.
- **Top Quality Audio**: Extracts lossless or high-bitrate MP3/FLAC music tracks.
- **Resolution Picker**: Automatically detects available resolutions (up to 4K) for each video.
- **Easy Setup**: No complex installations—just pure Python power.

## Prerequisites

### 1. Python
Install **Python 3.10+** from [python.org](https://www.python.org/downloads/).

> **Windows users**: Make sure to check ✅ **"Add Python to PATH"** during installation.

### 2. FFmpeg (required for audio extraction & video merging)

**Windows:**
1. Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) (select a Windows build).
2. Extract the archive and copy the `bin` folder contents to `C:\ffmpeg\bin\`.
3. Add `C:\ffmpeg\bin` to your system `PATH` environment variable.

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Linux (apt):**
```bash
sudo apt update && sudo apt install ffmpeg
```

### 3. Python Dependencies
Install all required packages with a single command:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install yt-dlp customtkinter Pillow
```

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/HappyBirdProduction/yt-downloader-pro.git
   cd yt-downloader-pro
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python downloader.py
   ```

4. Paste a YouTube URL, click **Check** to load formats, select your desired resolution or audio settings, choose the output folder, and hit **DOWNLOAD**!

## Custom Logo
To use a custom logo, place a `logo.png` file in the same directory as `downloader.py`. If no logo is found, the app displays a text title instead.

## Troubleshooting

| Problem | Solution |
|---|---|
| `ffmpeg` not found | Make sure FFmpeg is installed and added to your system PATH |
| No audio in downloaded video | Install/update FFmpeg — it's required for merging audio + video streams |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` to install all dependencies |
| App crashes on download error | Fixed in v1.1 — update to the latest version |

## License
MIT License — free for personal and commercial use.

---
*Brought to you by [aiBlackBox](https://aiblackbox.co.uk/). Follow us for more AI toolkits and autonomous engineering insights!*
