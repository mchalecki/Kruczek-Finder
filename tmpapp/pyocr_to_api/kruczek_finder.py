import random

from tqdm import tqdm

from .search_text import search_for_phrase
from .document_marking import DocumentMarking
from .ocr_processer import OCRProcessor
from ..tmpdatasource.source import DataSource
import uuid
import json

DEFAULT_MARKER = DocumentMarking()
DEFAULT_OCR_PROCESSOR = OCRProcessor()


class KruczekFinder:
    def __init__(
            self,
            class_found_clause,
            class_image,
            data_source,
            marker=DEFAULT_MARKER,
            ocr_processor=DEFAULT_OCR_PROCESSOR,
    ):
        self.class_image = class_image,
        self.class_found_clause = class_found_clause,
        self._data_source = data_source
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

        if p1y > p2y > p3y > p4y or p3y > p4y > p1y > p2y:
            return [area1, area2]
        elif p1y >= p3y and p4y >= p2y:
            return (min(p1x, p3x), p1y), (max(p2x, p4x), p4y)
        elif p3y >= p4y and p1y >= p2y:
            return (min(p3x, p1x), p3y), (max(p4x, p2x), p2y)
        elif p1y >= p3y and p2y <= p4y:
            return p1, p2
        elif p3y >= p1y and p4y <= p2y:
            return p3, p4

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
        for phrase in self._data_source.data_for_categories(categories):
            parts_to_mark.extend(search_for_phrase(page_text, phrase))
        return parts_to_mark

    def process_file(self, path, categories):
        # images_marked = []
        # colors = {}
        data = {}
        images = []
        for image, page_text in tqdm(self._ocr.process(path)):
            extension = path.split('.')[-1]
            new_path = path.replace(extension, uuid.uuid4().hex + '.jpg')
            image.save(new_path)
            data[new_path] = []

            parts_to_mark = self._process_page(
                page_text,
                self._category_wrapper(categories),
            )

            # _image = image
            phrases = {}
            data = {}
            phrase_objects = {}
            value = []
            for mark_phrase in parts_to_mark:
                phrase, area = mark_phrase
                # print('area', area)
                value = phrases.get(phrase.postanowienie_wzorca, [])
                value.append(area)
                phrases[phrase.postanowienie_wzorca] = value
                phrase_objects[phrase.postanowienie_wzorca] = phrase
            for key in phrases:
                reduced = self.reduce_areas(phrases[key])
                # print('reduced', reduced)
                for area in reduced:
                    # print(area)
                    # if key not in colors:
                    #     r = lambda: random.randint(0, 255)
                    #     colors[key] = (r(), r(), r())
                    # _image = self._marker.mark(
                    #     image_object=_image,
                    #     position=area,
                    #     color=colors[key],
                    # )
                    value = data.get(new_path, {})
                    value_dict = value.get(key, [])
                    value_dict.append(area)
            for path in value:
                img = self.class_image(path=path)
                img.save()
                images.append(img)
                clauses_raw = value[path]
                for clause_name in clauses_raw:
                    clause = phrase_objects[clause_name]
                    positions = clauses_raw[clause_name]
                    self.class_found_clause(clause, img, json.dumps(positions)).save()

                    # images_marked.append(_image)
                    # _image.show()
        return images

    def _category_wrapper(self, category):
        if isinstance(category, list) or isinstance(category, tuple):
            return category
        return [category]
