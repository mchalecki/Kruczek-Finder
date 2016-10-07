from multiprocessing import Process, Manager
import os
import uuid

from django.conf import settings
from django.core.mail import send_mail
from django import db

from .models import Session

from tmpapp.pyocr_to_api.kruczek_finder import KruczekFinder


class ProcessorMock(object):
    """
    Just for now.
    """

    def process(self, fname, categories):
        return [1, 2]


class DocumentsHandler(object):
    """
    Handler for documents obtained from users.
    """

    def __init__(self, email, documents, domain):
        """
        Handle email and files obtained from user.
        """
        self.user_email = email
        self.domain = domain
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

    def get_finder_instance(self):
        """
        Avoiding recursive import
        """
        from .models import Clause, FoundClause, Image

        datasource = Clause.objects
        return KruczekFinder(
            FoundClause, Image, datasource
        )

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

    def handle_file(self, file, categories):
        """
        Callable that handles single file.
        Executed by multiprocessing worker.
        """
        finder = self.get_finder_instance()
        finder_result = finder.process_file(file, categories)
        return finder_result

    def _run(self):
        """
        Runs workers.
        This method may (and will) take long time to return.
        """
        manager = Manager()
        workers = []
        results = []
        for file, categories in self.user_files:
            result = self.handle_file(file, categories)
            results.append(result)
        self.handle_results(results)

    def handle_results(self, results):
        """
        Return results to ResultsHandler
        """
        results = [list(r) for r in results]
        results_handler = ResultsHandler(results, self.user_email, self.domain)
        results_handler.process_results()

    def process_files(self):
        """
        Runs workers in separate thread. Returns immediately.
        """
        db.connections.close_all()
        p = Process(target=self._run)
        p.start()


class ResultsHandler(object):
    """
    Handler for results received from OCR.
    """

    def __init__(self, results, email, domain):
        self.results = results
        self.email = email
        self.domain = domain
        self.session = Session.objects.create()

    def get_url(self):
        return 'http://'+os.path.join(self.domain, self.session.token)

    def send_mail(self):
        send_mail(
            subject="KruczekFinder - wyniki analizy",
            message="""
                Witaj!
                Dziękujemy za skorzystanie z usługi KruczekFinder.
                Wyniki analizy swojej umowy znajdziesz pod adresem:
                %s
            """ % (self.get_url()),
            from_email='kruczekfinder@mail.com',
            recipient_list=[self.email],
            fail_silently=False,

        )

    def process_results(self):
        for images in self.results:
            for image in images:
                image.session = self.session
                image.save()
        self.send_mail()
