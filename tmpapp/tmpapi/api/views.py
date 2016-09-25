from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView

from .forms import CredentialsForm, DocumentsFormset
from .handler import DocumentsHandler


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

        documents_handler = DocumentsHandler(self.email, documents)
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
