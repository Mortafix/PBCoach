from asyncio import get_event_loop

from yt_dlp import YoutubeDL


def run_download(url, opts):
    with YoutubeDL(opts) as ydl:
        ydl.download([url])


async def download_async(url, opts):
    loop = get_event_loop()
    return await loop.run_in_executor(None, run_download, url, opts)


async def download_clip(video_id, start, end, filename):
    url = f"https://stream.mux.com/{video_id}.m3u8"
    ffmpeg_options = {
        "-ss": str(start),
        "-to": str(end),
        "-c": "copy",
        "-movflags": "+faststart",
    }
    options = {
        "outtmpl": filename,
        "merge_output_format": "mp4",
        "format": (
            "bestvideo[height=1080][vcodec*=avc1]/"
            "bestvideo[height=1080][vcodec*=h264]/"
            "bestvideo[height>=1080][vcodec*=h264]/"
            "bestvideo[vcodec*=h264]/best"
            " +bestaudio/best"
        ),
        "retries": 5,
        "fragment_retries": 5,
        "external_downloader": "ffmpeg",
        "external_downloader_args": {
            "ffmpeg": [
                param for key, val in ffmpeg_options.items() for param in (key, val)
            ],
        },
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "verbose": False,
        "overwrites": True,
    }
    await download_async(url, options)
