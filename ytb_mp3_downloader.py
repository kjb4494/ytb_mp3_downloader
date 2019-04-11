from youtube_dl import YoutubeDL
from moviepy.editor import VideoFileClip
import os
import argparse

download_path = 'downloads/'
audio_files_path = download_path + 'audio/'
video_files_path = download_path + 'video/'


def youtube_downloader(url):
    ydl_options = {
        'outtmpl': video_files_path + '%(title)s.%(ext)s'
    }
    ydl = YoutubeDL(ydl_options)
    ydl.add_default_info_extractors()
    info = ydl.extract_info(
        url=url,
        download=True,
    )
    return ydl.prepare_filename(info)


def mp4_to_mp3_encoder(file_name, args_type):
    if args_type == 'vo':
        return
    clip = VideoFileClip(file_name)
    clip.audio.write_audiofile(file_name.replace('.mp4', '.mp3').replace(video_files_path, audio_files_path))
    if args_type == 'ao':
        os.remove(file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='youtube file downloader')
    parser.add_argument(dest='URL')
    parser.add_argument('-t', '--type',
                        choices=['ao', 'vo'],
                        help='If is not set, download audio and video all. '
                             '\'ao\' download audio file only and '
                             '\'vo\' download video file only')
    args = parser.parse_args()
    if not os.path.exists(download_path):
        print('Path not exist for downloads. Create "' + download_path + '" directory.')
        os.makedirs(download_path)
    if not os.path.exists(audio_files_path):
        print('Path not exist for Audio files. Create "' + audio_files_path + '" directory.')
        os.makedirs(audio_files_path)
    if not os.path.exists(video_files_path):
        print('Path not exist for Video files. Create "' + video_files_path + '" directory.')
        os.makedirs(video_files_path)
    try:
        mp4_to_mp3_encoder(youtube_downloader(args.URL), args.type)
    except KeyboardInterrupt:
        print('Keyboard Interrupted Exit')
    except Exception as e:
        print(e)
