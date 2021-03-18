import argparse
import time
import urllib
from pathlib import Path

import requests
from imagededup.methods import CNN
from tqdm import tqdm


def get_images(board, width, height):
    """
    Get images of size (width, height) from board
    """

    page = requests.get(f"https://a.4cdn.org/{board}/catalog.json")
    thread_nos = [x["no"] for y in page.json() for x in y["threads"]]
    filenames = []
    for thread in tqdm(thread_nos, desc="Getting threads"):
        thread_content = requests.get(
            f"https://a.4cdn.org/{board}/thread/{thread}.json"
        )
        for post_content in thread_content.json()["posts"]:
            if (
                'h' in post_content
                and post_content['w'] == width
                and post_content['h'] == height
            ):
                attachment_timestamp = post_content["tim"]
                attachment_ext = post_content["ext"]
                filename = f"{attachment_timestamp}{attachment_ext}"
                filenames.append(filename)
        time.sleep(1)
    download_bar = tqdm(filenames)
    for name in download_bar:
        image_url = f"https://i.4cdn.org/{board}/{name}"
        if Path(name).is_file():
            download_bar.set_description(desc=f"{name} exists")
        else:
            urllib.request.urlretrieve(image_url, name)
            download_bar.set_description(desc=f"{name} downloaded")
        time.sleep(1)
    print("Finished")


def main():
    """
    Main process
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--board",
        help="target board to scrape images from",
        type=str,
        required=True,
        dest="board",
    )
    parser.add_argument(
        "--width",
        help="width of the images you wish to download",
        type=int,
        required=True,
        dest="width",
    )
    parser.add_argument(
        "--height",
        help="height of the images you wish to download",
        type=int,
        required=True,
        dest="height",
    )
    parser.add_argument(
        "--similarity",
        help="minimum similarity threshold to delete duplicate images. Must be between 0 and 1.",
        type=float,
        required=True,
        dest="similarity",
    )
    args = parser.parse_args()
    board = args.board
    width = args.width
    height = args.height
    similarity = args.similarity
    print("Welcome to cloverwallpaper your loaded parameters are:")
    print(f"Board: {args.board}")
    print(f"Width: {args.width}")
    print(f"Height: {args.height}")
    print(f"Similarity: {args.similarity}")
    get_images(board, width, height)
    print("Removing duplicate images")

    cnn_encoder = CNN()
    duplicates = cnn_encoder.find_duplicates_to_remove(
        image_dir=".", min_similarity_threshold=similarity
    )
    for file_name in duplicates:
        if Path(file_name).is_file():
            Path(file_name).unlink()
    print(f"Removed {len(duplicates)} files")
    print("Finished")


if __name__ == "__main__":
    main()
