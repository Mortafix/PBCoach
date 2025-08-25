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
    ffmpeg_args = {
        "-ss": f"{start:.3f}",
        "-t": f"{end - start:.3f}",
        "-c": "copy",
        "-start_at_zero": "",
        "-movflags": "+faststart",
    }
    options = {
        "outtmpl": filename,
        "merge_output_format": "mp4",
        "format": "bv*+ba/best",
        "retries": 5,
        "fragment_retries": 5,
        "external_downloader": "ffmpeg",
        "external_downloader_args": {
            "ffmpeg": [p for el in ffmpeg_args.items() for p in el if p]
        },
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "verbose": False,
        "overwrites": True,
    }
    await download_async(url, options)
