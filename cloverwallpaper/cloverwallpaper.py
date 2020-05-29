import argparse
import sys
import time
import urllib
from pathlib import Path

import cv2
import requests
from skimage import io
from skimage.metrics import structural_similarity
from tqdm import tqdm


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
    for y_image in cwd.glob("*.jpg"):
        y_image = io.imread(y_image)
        if y_image.shape == x_image.shape:
            ssim = structural_similarity(x_image, y_image, multichannel=True)
            if ssim > 0.80:
                return True
    for y_image in cwd.glob("*.png"):
        y_image = io.imread(y_image)
        if y_image.shape == x_image.shape:
            ssim = structural_similarity(x_image, y_image, multichannel=True)
            if ssim > 0.80:
                return True
    return False


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
    args = parser.parse_args()
    board = args.board
    width = args.width
    height = args.height
    print("Welcome to cloverwallpaper your loaded parameters are:")
    print(f"Board: {args.board}")
    print(f"Width: {args.width}")
    print(f"Height: {args.height}")
    get_images(board, width, height)


if __name__ == "__main__":
    main()
