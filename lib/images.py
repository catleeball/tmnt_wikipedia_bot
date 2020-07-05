import subprocess
import sys
from lib.constants import URL, WSS, SCREENSHOT_PATH

def getLogo(title: str, compress: bool = True, format_img: bool = True):
    # Logo webpage interprets underscores in URL argument as spaces.
    title = title.replace(" ", "_")

    wss_cmd = f'{WSS} --quiet "{URL}#{title}" {SCREENSHOT_PATH}'
    retcode = subprocess.run(wss_cmd, shell=True).returncode
    if retcode != 0:
        sys.stderr.write(f"[ERROR]: wss exit code {retcode}")
        sys.exit(1)

    if format_img:
        _cropLogo(SCREENSHOT_PATH)
        _addBorder(SCREENSHOT_PATH)
    if compress:
        _compressPng(SCREENSHOT_PATH)

    return SCREENSHOT_PATH

def _cropLogo(path=SCREENSHOT_PATH):
    # http://www.imagemagick.org/Usage/crop/#trim
    # Don't exit on subprocess error, image likely still in place and undamaged.
    cmd = f"convert {SCREENSHOT_PATH} -quiet -trim +repage {SCREENSHOT_PATH}"
    retcode = subprocess.run(cmd, shell=True).returncode
    if retcode != 0:
        sys.stderr.write(f"[ERROR]: imagemagick -trim exit code {retcode}")
        sys.stderr.flush()

def _addBorder(path=SCREENSHOT_PATH):
    # http://www.imagemagick.org/Usage/crop/#border
    # Don't exit on subprocess error, image likely still in place and undamaged.
    cmd = f'convert "{SCREENSHOT_PATH}" -quiet -border 20%x10% -bordercolor white "{SCREENSHOT_PATH}"'
    retcode = subprocess.run(cmd, shell=True).returncode
    if retcode != 0:
        sys.stderr.write(f"[ERROR]: imagemagick -border exit code {retcode}")
        sys.stderr.flush()

def _compressPng(path=SCREENSHOT_PATH):
    # https://github.com/google/zopfli
    # Don't exit on subprocess error, image likely still in place and undamaged.
    cmd = f"/usr/bin/zopflipng -m -y --lossy_8bit --lossy_transparent {path} {path} &> /dev/null"
    retcode = subprocess.run(cmd, shell=True).returncode
    if retcode != 0:
        sys.stderr.write(f"[ERROR]: zopfli exit code {retcode}")
        sys.stderr.flush()

