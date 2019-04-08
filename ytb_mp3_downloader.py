from youtube_dl import YoutubeDL
from moviepy.editor import VideoFileClip
import os
import argparse


def filter_file_name(file_name):
    for filter_char in ['\\', '/', ':', '*', '?', '"', '|', '>', '<']:
        file_name = file_name.replace(filter_char, '')
    return file_name


def youtube_downloader(url):
    ydl = YoutubeDL()
    ydl.add_default_info_extractors()
    info = ydl.extract_info(
        url=url,
        download=True,
    )
    file_name = filter_file_name(info.get('title') + '-' + info.get('webpage_url_basename') + '.mp4')
    filtered_file_name = file_name.replace('-' + info.get('webpage_url_basename'), '')
    os.rename(file_name, filtered_file_name)
    return filtered_file_name


def mp4_to_mp3_encoder(file_name, no_delete_mp4_file, output_file_name):
    clip = VideoFileClip(file_name)
    new_file_name = file_name.replace('.mp4', '.mp3') \
        if output_file_name is None else filter_file_name(output_file_name) + '.mp3'
    clip.audio.write_audiofile(new_file_name)
    if not no_delete_mp4_file:
        os.remove(file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='youtube file downloader')
    parser.add_argument(dest='URL')
    parser.add_argument('-nd', '--no-delete',
                        help='Do not delete temporary mp4 file',
                        action='store_true')
    parser.add_argument('-o', '--output',
                        help='Encoded mp3 filename')

    args = parser.parse_args()

    try:
        mp4_to_mp3_encoder(youtube_downloader(args.URL), args.no_delete, args.output)
    except KeyboardInterrupt:
        print('Keyboard Interrupted Exit')
    except Exception as e:
        print(e)
