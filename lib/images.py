import subprocess
import sys

from lib.constants import LOGO_PATH
from lib.constants import CHROME_PATH
from PIL import Image, ImageChops


def getLogo(title: str, chrome=CHROME_PATH):
    title = title.replace(" ", "_")

    # TODO: Generate logo locally, stop hitting glench.com (sorry glench)
    chrome_cmd = (
        f"{chrome} "
        "--headless "
        "--disable-gpu "
        "--screenshot "
        "--window-size=1280,600 "
        f'"http://glench.com/tmnt/#{title}"'
    )

    retcode = subprocess.run(chrome_cmd, shell=True).returncode
    if retcode != 0:
        sys.stderr.write(f"Chrome subprocess exited with code {retcode}")
        sys.exit(1)

    screesnhot_path = "screenshot.png"
    logo_path = _cropLogo(screesnhot_path)
    return logo_path


def _trimWhitespace(im):
    # calculate bbox of image area
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()

    if bbox:
        # crop the image and store sizes as variables
        croppedImage = im.crop(bbox)
        croppedImageWidth = croppedImage.size[0]
        croppedImageHeight = croppedImage.size[1]

        # calculate size of output image based on width of cropped image,
        # 1:1.9 aspect ratio, and side margin pixels
        SIDE_MARGIN = 30
        outputImageWidth = croppedImageWidth + (SIDE_MARGIN * 2)
        outputImageHeight = int(outputImageWidth * 0.52632)
        outputImageSize = tuple([outputImageWidth, outputImageHeight])

        # create empty image
        outputImage = Image.new(im.mode, outputImageSize, im.getpixel((0, 0)))

        # calculate positioning of cropped image on empty background, paste
        x = SIDE_MARGIN
        y = int((outputImageHeight - croppedImageHeight) / 2)
        outputImage.paste(croppedImage, (x, y))

        return outputImage

def _cropOffTopAndBottom(image_path: str):
    im = Image.open(image_path)
    w, h = im.size
    return im.crop((0, 175, w, h - 100))


def _cropLogo(im):
    logo_path = LOGO_PATH
    im = _cropOffTopAndBottom(im)
    im = _trimWhitespace(im)
    im.save(logo_path)
    return logo_path
