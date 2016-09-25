from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, TemplateView

from .forms import CredentialsForm, DocumentsFormset
from .handler import DocumentsHandler
from .models import Image, Session


class MainView(FormView):
    """
    Pretty simple:
    - homepage with form on GET
    - all of the *magic* stuff on POST
    """
    template_name = 'home.html'
    thanks_template_name = 'thanks.html'

    form_class = CredentialsForm

    def get_context_data(self, *args, **kwargs):
        """
        Updates context with formsets containing file inputs.
        """
        kwargs['formset'] = DocumentsFormset()
        return super(MainView, self).get_context_data(*args, **kwargs)

    def form_valid(self, form, formset):
        """
        Handle valid forms.
        """
        self.email = form.cleaned_data['email']
        documents = [
            (form.cleaned_data['document'], form.cleaned_data['categories'])
            for form in formset.forms
        ]
        domain = self.request.META['HTTP_HOST']

        documents_handler = DocumentsHandler(self.email, documents, domain)
        documents_handler.process_files()

        return self.thank_user()

    def thank_user(self):
        return render(
            self.request, self.thanks_template_name,
            self.get_context_data(
                email=self.email
            )
        )

    def form_invalid(self, form, formset):
        """
        Return with proper error message.
        """
        return self.render_to_response(self.get_context_data(
            form=form,
            formset=formset
        ))

    def post(self, request, *args, **kwargs):
        """
        Initialize forms with sent data.
        """
        form = self.get_form()
        formset = DocumentsFormset(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)


class ResultView(TemplateView):
    """
    View for presenting analysis result.
    """

    template_name = 'result.html'

    def get(self, *args, **kwargs):
        session = get_object_or_404(Session, token=kwargs.pop('token'))
        try:
            images = Image.objects.filter(session=session)
        except AttributeError:
            print("no")
            images = []

        return self.render_to_response(
            self.get_context_data(images=images)
        )
