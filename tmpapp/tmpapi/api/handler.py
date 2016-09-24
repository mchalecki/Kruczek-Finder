from multiprocessing import Process, Manager
import os
import uuid

from django.conf import settings

from tmpapp.pyocr_to_api.ocr_processer import OCRProcesser


class ProcessorMock(object):
    """
    Just for now.
    """

    def process(self, fname, categories):
        return {
            'fname': fname,
            'status': 'OK'
        }


class DocumentsHandler(object):
    """
    Handler for documents obtained from users.
    """

    def __init__(self, email, documents):
        """
        Handle email and files obtained from user.
        """
        self.user_email = email
        # temporary save files
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)
        self.user_files = [
            (self.save_as_tmp(file), categories)
            for file, categories in documents
        ]

    @property
    def tmp_dir(self):
        return settings.TMP_DIR

    def get_procsser_instance(self):
        return ProcessorMock()

    def get_tmp_name(self, fname):
        """
        Generates temporary name for given filename.
        """
        fname, ext = os.path.splitext(fname)
        tmp_name = fname + str(uuid.uuid4()) + ext
        return tmp_name

    def save_as_tmp(self, file):
        """
        Temporary saves given file on server (for processing).
        Returns filename of created copy.
        """
        fpath = os.path.join(self.tmp_dir, self.get_tmp_name(file.name))
        with open(fpath, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return fpath

    def handle_file(self, file, categories, result):
        """
        Callable that handles single file.
        Executed by multiprocessing worker.
        """
        processer = self.get_procsser_instance()
        processing_result = processer.process(file, categories)
        result.update(processing_result)

    def _run(self):
        """
        Runs workers.
        This method may (and will) take long time to return.
        """
        manager = Manager()
        workers = []
        results = []

        for file, categories in self.user_files:
            result = manager.dict()
            results.append(result)
            worker = Process(
                target=self.handle_file, args=(file, categories, result)
            )
            workers.append(worker)
            worker.start()
        # join all the workers
        for worker in workers:
            worker.join()
        # and handle results
        self.handle_results(results)

    def handle_results(self, results):
        """
        Just print it to the console.
        Enough for the demo, lol
        """
        def proxy_dict_to_dict(proxy_dict):
            """ This is stupid, but dict(proxy_dict) doesn't work... """
            return {k: v for k, v in proxy_dict.items()}

        from pprint import pprint
        results = [proxy_dict_to_dict(result) for result in results]
        pprint(results)

    def process_files(self):
        """
        Runs workers in separate thread. Returns immediately.
        """
        p = Process(target=self._run)
        p.start()
