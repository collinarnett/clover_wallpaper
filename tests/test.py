import uuid
from pathlib import Path

from cloverwallpaper.cloverwallpaper import get_images


def test_ssim():
    """
    test_ssim functionality
    """

    # Get inital pool of images
    get_images("wg", 3440, 1440)

    # Shuffle image names
    for img in Path.cwd().glob("*.jpg|*.png"):
        random_string = uuid.uuid4().hex.upper()
        img.rename(f"{random_string}{img.suffix}")

    # Get images again to test ssim
    get_images("wg", 3440, 1440)


test_ssim()
