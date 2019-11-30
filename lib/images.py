import subprocess
import sys

from lib.constants import LOGO_PATH, CHROME_PATH, SCREENSHOT_PATH
from PIL import Image, ImageChops


def getLogo(title: str, chrome=CHROME_PATH):
    title = title.replace(" ", "_")

    # TODO: Generate logo locally, stop hitting glench.com (sorry glench)
    chrome_cmd = (
        f"{chrome} "
        "--headless "
        "--disable-gpu "
        f"--screenshot={SCREENSHOT_PATH} "
        "--window-size=1280,600 "
        f'"http://glench.com/tmnt/#{title}"'
    )

    retcode = subprocess.run(chrome_cmd, shell=True).returncode
    if retcode != 0:
        sys.stderr.write(f"Chrome subprocess exited with code {retcode}")
        sys.exit(1)

    logo_path = _cropLogo(SCREENSHOT_PATH)
    _ = _compressPng(logo_path)
    return logo_path


def _compressPng(path):
    cmd = f"/usr/bin/zopflipng -m -y --lossy_8bit --lossy_transparent {path} {path}"
    retcode = subprocess.run(cmd, shell=True).returncode
    if retcode != 0:
        sys.stderr.write(f"zopfli subprocess exited with code {retcode}")
    return True

def _convertToWebp(path):
    cwebp_cmd = f"/usr/bin/cwebp -q 60 -mt -m 6 -af {path} -o {path}.webp"
    retcode = subprocess.run(cwebp_cmd, shell=True).returncode
    if retcode != 0:
        sys.stderr.write(f"cwebp subprocess exited with code {retcode}")
        # Not a critical error, just return the png
        return path

    logo_path = f"{path}.webp"
    sys.stderr.write(f"path is {logo_path}")
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
