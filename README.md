# YouTube Video Downloader

A simple command-line **YouTube Video Downloader** built with Python and [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).

The program fetches available video formats from a YouTube URL, displays information such as resolution, FPS, format, audio availability, and estimated file size, and allows the user to choose a specific format or download the best available quality.

## Features

- Fetch video information directly from a YouTube URL
- Display available video formats
- Show:
  - Resolution
  - FPS
  - File format
  - Audio availability
  - Estimated file size
- Select a specific video quality
- Automatically download the best quality using option `0`
- Automatically combine video-only formats with the best available audio
- Merge video and audio into an MP4 file
- Prevent accidental overwriting of existing downloads
- Save downloaded videos inside a dedicated `downloads` folder
- Simple command-line interface

## Requirements

Make sure you have **Python 3** installed.

The project requires:

- Python
- yt-dlp
- FFmpeg

### Install yt-dlp

```bash
pip install yt-dlp
```

### Install FFmpeg

FFmpeg is required when separate video and audio streams need to be merged.

Download FFmpeg from:

https://ffmpeg.org/download.html

Make sure FFmpeg is added to your system's `PATH`.

You can verify the installation using:

```bash
ffmpeg -version
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
```

Move into the project directory:

```bash
cd YOUR_REPOSITORY_NAME
```

Install the required Python package:

```bash
pip install yt-dlp
```

## Usage

Run the program:

```bash
python downloader.py
```

Enter a YouTube URL when prompted:

```text
==================================================
       YouTube Video Downloader
==================================================

Enter YouTube URL: https://www.youtube.com/watch?v=XXXXXXXXXXX
```

The program will fetch the video information and display the available formats.

Example:

```text
Available video formats:

No.  Format ID   Ext     Resolution     FPS    Audio     Size
----------------------------------------------------------------
1    137         mp4     1920x1080      30     No        45.2 MB
2    136         mp4     1280x720       30     No        24.8 MB
3    135         mp4     854x480        30     No        12.5 MB
```

Choose the number corresponding to the format you want:

```text
Enter format number (or 0 for best quality): 1
```

Or enter:

```text
0
```

to automatically download the best available video and audio quality.

## How It Works

The program first retrieves metadata and available formats using `yt-dlp`.

When a format already contains both video and audio, that format is downloaded directly.

When the selected format contains only video, the program automatically adds the best available audio stream:

```text
Selected Video + Best Audio
```

For the best-quality option, the program uses:

```text
bestvideo+bestaudio/best
```

The streams are then merged into an MP4 file when necessary.

## Download Location

Downloaded files are automatically stored in:

```text
downloads/
```

The folder is created automatically if it does not already exist.

Example project structure:

```text
youtube-video-downloader/
│
├── downloader.py
├── README.md
└── downloads/
    └── downloaded_video.mp4
```

## Notes

- The program downloads one video at a time.
- Playlist downloading is disabled.
- Existing files are not overwritten automatically.
- Available resolutions and formats depend on the video.
- High-resolution YouTube videos commonly provide video and audio as separate streams, so FFmpeg may be required to merge them.

## Technologies Used

- **Python**
- **yt-dlp**
- **FFmpeg**

## Disclaimer

This project is intended for educational and personal use.

Users are responsible for ensuring that downloaded content complies with YouTube's Terms of Service, copyright laws, and the rights of content owners.

## License

This project is available for educational and personal use.
