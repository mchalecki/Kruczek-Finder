from PIL import Image

class ImageProcesser:
    def __init__(self, target_filetype='jpeg', target_resolution=600):
        self._target_filetype = target_filetype
        self._target_resolution = target_resolution

    def open(self, pdf_file):
        yield Image.open(pdf_file)
