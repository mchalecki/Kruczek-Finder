import io

from wand.image import Image as PDFImage
from PIL import Image


class PDFProcesser:
    def __init__(self, target_filetype='jpeg', target_resolution=600):
        self._target_filetype = target_filetype
        self._target_resolution = target_resolution

    def _pdf_to_image(self, path):
        return PDFImage(filename=path, resolution=self._target_resolution)

    def _convert(self, pdf):
        return pdf.convert(self._target_filetype)

    def _get_list_of_images(self, pdf):
        return [PDFImage(image=img).make_blob('jpeg') for img in pdf.sequence]

    def open(self, pdf_file):
        pdf = self._pdf_to_image(pdf_file)
        for pdf_page in self._get_list_of_images(pdf):
            yield Image.open(io.BytesIO(img))

if __name__ == '__main__':
    fname = 'sample_files/Wzor_umowy_KG_zawieranej_w_formie_elektronicznej_trybie_za_posrednictwem_mLinii.pdf'
    pdfp = PDFProcesser()
    p = pdfp.open(fname)
    # print(p)
