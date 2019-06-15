import subprocess
import sys

from PIL import Image, ImageChops


def getLogo(title: str):
    title = title.replace(" ", "_")

    chrome_cmd = (
        "google-chrome-beta "
        "--headless "
        "--disable-gpu "
        "--screenshot "
        "--window-size=1280,600 "
        f'"http://glench.com/tmnt/#{title}"'
    )

    retcode = subprocess.run(chrome_cmd, shell=True).returncode
    if retcode != 0:
        sys.stderr.write("Chrome subprocess exited with code 1")
        sys.exit(1)

    screesnhot_path = "screenshot.png"
    logo_path = _cropLogo(screesnhot_path)
    return logo_path


def _trimWhitespace(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def _cropOffTopAndBottom(image_path: str):
    im = Image.open(image_path)
    w, h = im.size
    return im.crop((0, 175, w, h - 100))


def _cropLogo(im):
    logo_path = "/tmp/logo.png"
    im = _cropOffTopAndBottom(im)
    im = _trimWhitespace(im)
    im.save(logo_path)
    return logo_path
