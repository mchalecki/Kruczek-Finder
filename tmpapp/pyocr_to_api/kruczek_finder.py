from tqdm import tqdm

from .search_text import search_for_phrase
from .document_marking import DocumentMarking
from .ocr_processer import OCRProcessor
from .tmpdatasource.source import DataSource


DEFAULT_DATA_SOURCE = DataSource()
DEFAULT_MARKER = DocumentMarking()
DEFAULT_OCR_PROCESSOR = OCRProcessor()


class KruczekFinder:
    def __init__(
            self,
            data_source=DEFAULT_DATA_SOURCE,
            marker=DEFAULT_MARKER,
            ocr_processor=DEFAULT_OCR_PROCESSOR,
            ):
        self._data_source = data_source
        self._marker = marker
        self._ocr = ocr_processor

    def _process_page(self, page_text, categories):
        parts_to_mark = []
        print(self._data_source.data_for_categories(categories))
        for phrase in self._data_source.data_for_categories(categories):
            parts_to_mark.extend(search_for_phrase(page_text, phrase))
        return parts_to_mark

    def process_file(self, path, categories):
        images_marked = []
        for image, page_text in tqdm(self._ocr.process(path)):
            parts_to_mark = self._process_page(
                    page_text,
                    self._category_wrapper(categories),
                )
            _image = image
            for mark_phrase in parts_to_mark:
                _, area, ratio = mark_phrase
                print(area)
                _image = self._marker.mark(
                        image_object=_image,
                        position=area,
                        ratio=ratio,
                        )
            images_marked.append(_image)
            print(_image.size)
            _image.show()
        return None

    def _category_wrapper(self, category):
        if isinstance(category, list) or isinstance(category, tuple):
            return category
        return [category]
