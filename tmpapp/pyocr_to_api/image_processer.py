from PIL import Image


class ImageProcesser:
    def __init__(self, target_filetype='jpeg'):
        self._target_filetype = target_filetype

    def open(self, image_file):
        yield Image.open(image_file)
