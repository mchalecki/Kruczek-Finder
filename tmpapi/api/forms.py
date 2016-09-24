from django import forms


class DocumentForm(forms.Form):
    document = forms.FileField()


class CredentialsForm(forms.Form):
    """
    Contains:
            - informations collected from user when accepting files.
    """
    email = forms.EmailField()


DocumentsFormset = forms.formset_factory(DocumentForm, extra=1)
