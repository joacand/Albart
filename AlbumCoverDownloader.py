#! py -3

import os
import sys
import re
import argparse
from mutagen.mp3 import MP3
from mutagen import MutagenError
from mutagen.easyid3 import EasyID3
from lib import GoogleImageDownloader


def main(args):
    args = parse_args(args)
    start_directory = args.directory
    google_image_downloader = GoogleImageDownloader.GoogleImageDownloader()

    for directory in os.listdir(start_directory):
        full_directory_path = os.path.join(start_directory, directory)

        print('\nTrying to download album art recursively from directory %s' % directory)
        download_image_recursively_for_directories(full_directory_path, google_image_downloader)

    sys.exit(0)


def download_image_recursively_for_directories(directory, google_image_downloader):
    directory_finished = False
    for file in os.listdir(directory):
        full_file_path = os.path.join(directory, file)
        if os.path.isdir(full_file_path):
            download_image_recursively_for_directories(full_file_path, google_image_downloader)
        elif not directory_finished:
            directory_finished = download_image_for_album_directory(directory, google_image_downloader)


def download_image_for_album_directory(album_directory, google_image_downloader):
    for file_name in os.listdir(album_directory):
        acceptable_ext = ['.jpg', '.jpeg', '.png']
        if os.path.splitext(file_name)[1] in acceptable_ext:
            print('Album art already exists for %s. Image name: %s' % (album_directory, file_name))
            return True

    image_downloaded = False
    for file_name in os.listdir(album_directory):
        file_path_full = os.path.join(album_directory, file_name)

        if os.path.splitext(file_name)[1] == '.mp3' and not image_downloaded:
            image_downloaded = download_image_for_mp3(file_path_full, album_directory, google_image_downloader)

    return True


def download_image_for_mp3(file_path_full, album_directory, google_image_downloader):
    try:
        audioinfo = get_information(file_path_full)
        query = ''
        for key in audioinfo:
            query += '%s ' % audioinfo.get(key)
        query = clean_query(query)
        print("Querying for: %s" % query)
        return google_image_downloader.download_image(query, album_directory, 'folder-front')
    except MutagenError:
        print('Mutagen error. Check permissions')
        return False


def get_information(filepath):
    audioinfo = {}
    audiofile = MP3(filepath, ID3=EasyID3)
    audioinfo['artist'] = get_artist(audiofile, filepath)
    audioinfo['album'] = get_album(audiofile, filepath)
    audioinfo['date'] = get_date(audiofile)
    return audioinfo


def get_artist(audiofile, filepath):
    if 'artist' in audiofile:
        return audiofile['artist'][0]
    return os.path.basename(os.path.abspath(os.path.join(filepath, '..', '..')))


def get_album(audiofile, filepath):
    if 'album' in audiofile:
        return audiofile['album'][0]
    return os.path.basename(os.path.abspath(os.path.join(filepath, '..')))


def get_date(audiofile):
    if 'date' in audiofile:
        return audiofile['date'][0]
    return ''


def clean_query(query):
    query = query.replace('å', 'a')
    query = query.replace('ä', 'a')
    query = query.replace('ö', 'o')
    query = query.replace('_', ' ').strip()
    query = re.sub('[^a-zA-Z0-9-_*. ]', '', query)
    return query


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="starting directory of recursive album art fetching", required=True)
    return parser.parse_args(args)


if __name__ == '__main__':
    main(sys.argv[1:])
