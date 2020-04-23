import argparse
import sys
import time
import urllib
from pathlib import Path

import requests
from tqdm import tqdm


def main(*argv):
    """
    Downloads images from a specific board with a specified width and height.
    """
    if not argv:
        argv = list(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument("--board", help='target board to scrape images from', type=str, required=True, dest='board')
    parser.add_argument("--height", help='height of the images you wish to download', type=int, required=True, dest='height')
    parser.add_argument("--width", help='width of the images you wish to download', type=int, required=True, dest='width')
    args = parser.parse_args(argv[1:])
    board = args.board
    width = args.width
    height = args.height
    page = requests.get(f'https://a.4cdn.org/{board}/catalog.json')
    thread_nos = [x['no'] for y in page.json() for x in y['threads']]
    filenames = []
    for thread in tqdm(thread_nos, desc="Getting threads"):
        thread_content = requests.get(f'https://a.4cdn.org/{board}/thread/{thread}.json')
        for post_content in thread_content.json()['posts']:
            if ('w' and 'h' in post_content) and (post_content['w'] == width and post_content['h'] == height):
                attachment_timestamp = post_content['tim']
                attachment_ext = post_content['ext']
                filename = f'{attachment_timestamp}{attachment_ext}'
                filenames.append(filename)
        time.sleep(1)
    for name in tqdm(filenames, desc='Downloading Images'):
        if Path(name).is_file():
            print("File exist")
        else:
            urllib.request.urlretrieve(f'https://i.4cdn.org/{board}/{name}', name)
            time.sleep(1)

if __name__ == '__main__':
    main(*sys.argv)
