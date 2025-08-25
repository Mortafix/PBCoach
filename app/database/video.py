import asyncio

import yt_dlp


def run_download(url, opts):
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])


async def download_async(url, opts):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, run_download, url, opts)


async def download_clip(video_id, start, end, filename):
    url = f"https://stream.mux.com/{video_id}.m3u8"
    options = {
        "outtmpl": filename,
        "merge_output_format": "mp4",
        "format": "bv*+ba/best",
        "retries": 5,
        "fragment_retries": 5,
        "external_downloader": "ffmpeg",
        "external_downloader_args": {
            # "ffmpeg_i": ["-hide_banner", "-loglevel", "error", "-nostats"],
            "ffmpeg": [
                "-ss",
                str(start),
                "-to",
                str(end),
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                "-movflags",
                "+faststart",
            ],
        },
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "verbose": False,
        "overwrites": True,
    }
    await download_async(url, options)
