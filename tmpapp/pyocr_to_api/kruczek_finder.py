import random

from tqdm import tqdm

from .search_text import search_for_phrase
from .document_marking import DocumentMarking
from .ocr_processer import OCRProcessor
from ..tmpdatasource.source import DataSource

DEFAULT_DATA_SOURCE = DataSource()
DEFAULT_MARKER = DocumentMarking()
DEFAULT_OCR_PROCESSOR = OCRProcessor()


class KruczekFinder:
    def __init__(
            self,
            found_clause_class,
            image_class,
            datasource,
            marker=DEFAULT_MARKER,
            ocr_processor=DEFAULT_OCR_PROCESSOR,
    ):
        self.found_clause_class = found_clause_class
        self.image_class = image_class
        self._data_source = datasource
        self._marker = marker
        self._ocr = ocr_processor

    def range_overlap(self, a_min, a_max, b_min, b_max):
        overlapping = True
        if (a_min > b_max) or (a_max < b_min):
            overlapping = False
        return overlapping

    def overlap(self, p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y):
        return self.range_overlap(p1x, p2x, p3x, p4x) and self.range_overlap(p2y, p1y, p4y, p3y)

    def compare_areas(self, area1, area2):
        p1, p2 = area1
        p3, p4 = area2

        p1x, p1y = p1
        p2x, p2y = p2
        p3x, p3y = p3
        p4x, p4y = p4

        if self.overlap(p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y):
            return (min(p1x, p3x), min(p1y, p3y)), (max(p2x, p4x), max(p2y, p4y))
        else:
            return area1, area2

            # if p1y > p2y > p3y > p4y or p3y > p4y > p1y > p2y:
            #     return [area1, area2]
            # elif p1y >= p3y and p4y >= p2y:
            #     return (min(p1x, p3x), p1y), (max(p2x, p4x), p4y)
            # elif p3y >= p4y and p1y >= p2y:
            #     return (min(p3x, p1x), p3y), (max(p4x, p2x), p2y)
            # elif p1y >= p3y and p2y <= p4y:
            #     return p1, p2
            # elif p3y >= p1y and p4y <= p2y:
            #     return p3, p4

    def reduce_areas(self, areas):
        reduced = areas
        if len(areas) > 1:
            reduced = [areas[0]]
            for area in areas[1:]:
                reduced = self.compare_areas(reduced[-1], area)
        if not isinstance(reduced, list):
            reduced = [reduced]
        return reduced

    def _process_page(self, page_text, categories):
        parts_to_mark = []
        for clause in self._data_source.data_for_categories(categories):
            parts_to_mark.extend(search_for_phrase(page_text, clause))
        return parts_to_mark

    def process_file(self, path, categories):
        images = []
        for i, (image, page_text) in tqdm(enumerate(self._ocr.process(path))):

            parts_to_mark = self._process_page(
                page_text,
                self._category_wrapper(categories),
            )

            old_file_name = "path.split('/')[-1].split('.')[0]"
            new_path = 'tmp/{}{}.jpg'.format(old_file_name, i)
            image.save(new_path)

            img = self.image_class(path=new_path)
            img.save()
            images.append(img)

            phrases = {}
            for mark_phrase in parts_to_mark:
                phrase, area = mark_phrase
                value = phrases.get(phrase, [])
                value.append(area)
                phrases[phrase] = value

            for key in phrases:
                reduced = self.reduce_areas(phrases[key])
                self.found_clause_class(clause=key, image=img, ocr_data=reduced).save()
            print(new_path, phrases)
        print(images)
        return images

    def _category_wrapper(self, category):
        if isinstance(category, list) or isinstance(category, tuple):
            return category
        return [category]
