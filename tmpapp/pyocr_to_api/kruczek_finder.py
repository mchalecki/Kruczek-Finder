from .search_text import search_for_phrase
from .SaosDAO import SaosDAO
from .document_marking import DocumentMarking
from .ocr_processer import OCRProcessor
import pyocr.builders
from tqdm import tqdm


class KruczekFinder:
    def __init__(self):
        self.dao = SaosDAO()
        self.marker = DocumentMarking()
        self.ocr = OCRProcessor(default_builder=pyocr.builders.LineBoxBuilder())

    def _process_page(self, page_text, category):
        parts_to_mark = []
        for phrase in self.dao.get_category(category):
            parts_to_mark.extend(search_for_phrase(page_text, phrase))
        return parts_to_mark

    def process_file(self, path, category):
        images_marked = []
        for image, page_text in tqdm(self.ocr.process(path)):
            parts_to_mark = self._process_page(page_text, category)
            _image = image
            for mark_phrase in parts_to_mark:
                _, area, _ = mark_phrase
                print(area)
                _image = self.marker.mark(image_object=_image, position=area, message='ERROR')
            images_marked.append(_image)
            print(_image.size)
            _image.show()

        return None
