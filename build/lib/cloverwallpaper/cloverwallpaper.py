import argparse
import sys
import time
import urllib
from pathlib import Path

import requests
from tqdm import tqdm

import cv2
from skimage import io
from skimage.metrics import structural_similarity


def check_images(x_image):
    """
    Check if images in the current directory are the same as downloaded image
    """
    cwd = Path.cwd()
    x_image = io.imread(x_image)
    # In case of grayScale images the len(img.shape) == 2
    if len(x_image.shape) > 2 and x_image.shape[2] == 4:
        # convert the image from RGBA2RGB
        x_image = cv2.cvtColor(x_image, cv2.COLOR_BGRA2BGR)
    for y_image in cwd.glob("*"):
        y_image = io.imread(y_image)
        if len(y_image.shape) > 2 and y_image.shape[2] == 4:
            # convert the image from RGBA2RGB
            y_image = cv2.cvtColor(y_image, cv2.COLOR_BGRA2BGR)
        ssim = structural_similarity(x_image, y_image, multichannel=True)
        if ssim > 0.80:
            return True
    return False


def main(*argv):
    """
    Downloads images from a specific board with a specified width and height.
    """
    if not argv:
        argv = list(sys.argv)

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
    args = parser.parse_args(argv[1:])
    board = args.board
    width = args.width
    height = args.height
    print("Welcome to cloverwallpaper your loaded parameters are:")
    print("Board: {args.board}")
    print("Width: {args.width}")
    print("Height: {args.height}")
    page = requests.get(f"https://a.4cdn.org/{board}/catalog.json")
    thread_nos = [x["no"] for y in page.json() for x in y["threads"]]
    filenames = []
    for thread in tqdm(thread_nos, desc="Getting threads"):
        thread_content = requests.get(
            f"https://a.4cdn.org/{board}/thread/{thread}.json"
        )
        for post_content in thread_content.json()["posts"]:
            if ("w" and "h" in post_content) and (
                post_content["w"] == width and post_content["h"] == height
            ):
                attachment_timestamp = post_content["tim"]
                attachment_ext = post_content["ext"]
                filename = f"{attachment_timestamp}{attachment_ext}"
                filenames.append(filename)
        time.sleep(1)
    download_bar = tqdm(filenames)
    for name in download_bar:
        image_url = f"https://i.4cdn.org/{board}/{name}"
        if Path(name).is_file() or check_images(image_url):
            download_bar.set_description(desc=f"{name} exists")
            time.sleep(1)
        else:
            urllib.request.urlretrieve(image_url, name)
            download_bar.set_description(desc=f"{name} downloaded")
            time.sleep(1)
    print("Finished")


if __name__ == "__main__":
    main(*sys.argv)
