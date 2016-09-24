import pyocr
import pyocr.builders

from utils import _get_default_ocr_tool
from pdf_processer import PDFProcesser
from image_processer import ImageProcesser

DEFAULT_BUILDER = pyocr.builders.TextBuilder()
DEFAULT_IMAGE_PROCESSER = ImageProcesser()
DEFAULT_OCR_TOOL = _get_default_ocr_tool()
DEFAULT_PDF_PROCESSER = PDFProcesser()
DEFAULT_DATA_PROCESSERS = {
        'pdf': DEFAULT_PDF_PROCESSER,
        'image': DEFAULT_IMAGE_PROCESSER,
    }


class OCRProcesser:
    def __init__(
            self,
            ocr_tool=DEFAULT_OCR_TOOL,
            lang='pol',
            default_builder=DEFAULT_BUILDER,
            data_processers=DEFAULT_DATA_PROCESSERS,
            ):
        self._ocr_tool = ocr_tool
        self._lang = lang if self._validate_lang(lang) else 'eng'
        self._default_builder = default_builder
        self._data_processer = data_processers

    def _validate_lang(self, lang):
        return lang in self._ocr_tool.get_available_languages()

    def _validate_tool(self, ocr_tool):
        return ocr_tool.is_available()

    def process(self, data_file, extension):
        data_processer = self._choose_data_processor(extension)
        text = list()
        for image in data_processer.open(data_file):
            text.append(
                    self._ocr_tool.image_to_string(
                        image=image,
                        lang=self._lang,
                        builder=self._default_builder,
                    ),
                )
        return text

    def _choose_data_processor(self, extension):
        return self._data_processer.get(
                extension,
                self._data_processer['image'],
            )


if __name__ == '__main__':
    from time import time

    res = dict()
    for tool in pyocr.get_available_tools():
        ocrp = OCRProcesser(tool)
        now = time()
        text = ocrp.process('sample_files/skan0002.gif', 'gif')
        res[str(tool)] = (time() - now) / 60.0
        # print('Processing time: ', res[str(tool)])
        # print('TEST:\n', text)

    for key, time in res.items():
        print(key, '\t\t', time)
