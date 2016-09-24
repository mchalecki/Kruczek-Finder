from PIL import Image
from .exceptions import FileFormatError


class ImageProcesser:
    def __init__(self, target_filetype='jpeg'):
        self._target_filetype = target_filetype

    def open(self, image_file):
        try:
            image = Image.open(image_file)
        except OSError:
            raise FileFormatError()
        else:
            yield image
