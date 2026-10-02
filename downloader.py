from pathlib import Path
import sys

import yt_dlp


# -----------------------------
# Configuration
# -----------------------------

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Set to True to allow only formats that use the requested container.
STRICT_CONTAINER = False


# -----------------------------
# Helpers
# -----------------------------

def get_video_info(url: str) -> dict:
    """Fetch video metadata and available formats."""
    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        return ydl.extract_info(url, download=False)


def format_size(size):
    if not size:
        return "Unknown"

    size = float(size)

    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024

    return f"{size:.1f} TB"


def get_video_formats(info: dict) -> list:
    """
    Return video formats that contain both video and audio.

    Also include video-only formats because YouTube commonly
    separates high-quality video and audio streams.
    """
    formats = info.get("formats", [])

    return [
        f for f in formats
        if f.get("vcodec") != "none"
        and f.get("height")
    ]


def show_formats(formats):
    print("\nAvailable video formats:\n")

    print(
        f"{'No.':<5}"
        f"{'Format ID':<12}"
        f"{'Ext':<8}"
        f"{'Resolution':<15}"
        f"{'FPS':<7}"
        f"{'Audio':<10}"
        f"{'Size':<12}"
    )

    print("-" * 80)

    for i, f in enumerate(formats, start=1):
        audio = "Yes" if f.get("acodec") != "none" else "No"

        resolution = (
            f"{f.get('width', '?')}x{f.get('height', '?')}"
        )

        print(
            f"{i:<5}"
            f"{f.get('format_id', '?'):<12}"
            f"{f.get('ext', '?'):<8}"
            f"{resolution:<15}"
            f"{str(f.get('fps', '?')):<7}"
            f"{audio:<10}"
            f"{format_size(f.get('filesize') or f.get('filesize_approx')):<12}"
        )


def select_format(formats):
    while True:
        choice = input(
            "\nEnter format number (or 0 for best quality): "
        ).strip()

        if choice == "0":
            return None

        try:
            index = int(choice) - 1

            if 0 <= index < len(formats):
                return formats[index]

        except ValueError:
            pass

        print("Invalid selection. Try again.")


# -----------------------------
# Download
# -----------------------------

def download_video(url: str):
    print("\nFetching video information...")

    try:
        info = get_video_info(url)
    except Exception as e:
        print(f"Could not fetch video: {e}")
        return

    title = info.get("title", "Unknown title")
    print(f"\nTitle: {title}")

    formats = get_video_formats(info)

    if not formats:
        print("No downloadable video formats found.")
        return

    # Remove duplicate-looking entries for a cleaner menu.
    # Keep all format IDs available for actual downloading.
    formats = sorted(
        formats,
        key=lambda f: (
            f.get("height") or 0,
            f.get("fps") or 0,
            f.get("tbr") or 0,
        ),
        reverse=True,
    )

    show_formats(formats)

    selected = select_format(formats)

    if selected is None:
        # Best video + best audio.
        format_selector = (
            "bestvideo+bestaudio/"
            "best"
        )
    else:
        format_id = selected["format_id"]

        # Selected format may already contain audio.
        # If it is video-only, add the best audio stream.
        if selected.get("acodec") != "none":
            format_selector = format_id
        else:
            format_selector = f"{format_id}+bestaudio"

    output_template = str(
        DOWNLOAD_DIR / "%(title)s.%(ext)s"
    )

    ydl_opts = {
        "format": format_selector,

        # Merge streams into a playable container.
        "merge_output_format": "mp4",

        "outtmpl": output_template,

        # Prevent overwriting existing downloads.
        "nooverwrites": True,

        "noplaylist": True,

        "quiet": False,
    }

    print("\nDownloading...")
    print(f"Format selector: {format_selector}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("\nDownload complete!")
        print(f"Saved in: {DOWNLOAD_DIR.resolve()}")

    except Exception as e:
        print(f"\nDownload failed: {e}")


# -----------------------------
# Main
# -----------------------------

def main():
    print("=" * 50)
    print("       YouTube Video Downloader")
    print("=" * 50)

    url = input("\nEnter YouTube URL: ").strip()

    if not url:
        print("No URL entered.")
        sys.exit(1)

    download_video(url)


if __name__ == "__main__":
    main()