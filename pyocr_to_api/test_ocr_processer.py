import pytest
import pyocr
from time import time

from ocr_processer import OCRProcesser

TOOLS = pyocr.get_available_tools()[0]

@pytest.fixture()
def ocr_processer():
    return OCRProcesser()

class TestOCRProcesser:
    def test_image_processing(
            self,
            ocr_processer,
            filename='sample_files/skan0002.gif',
        ):
        now = time()
        text = ocr_processer.process(filename, 'gif')
        t = (time() - now) / 60.0
        print('Processing time: ', t)
        print('TEST:\n', text)
        assert text[0].startswith('Sygnatura akt I C 1127/13')

    @pytest.mark.skip()
    def test_pdf_processing(
            self,
            ocr_processer,
            filename='sample_files/Wzor_umowy_KG_zawieranej_w_formie_elektronicznej_trybie_za_posrednictwem_mLinii.pdf',
        ):
        now = time()
        text = ocr_processer.process(filename, 'pdf')
        t = (time() - now) / 60.0
        print('Processing time: ', t)
        print('TEST:\n', text)
        assert 'siedzibą w Warszawie przy ul. Senatorskiej 18,' in ''.join(text)
