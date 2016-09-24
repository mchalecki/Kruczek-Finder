from django import forms


MOCK_CHOICES = (
	('a', 'A'),
	('b', 'B'),
	('c', 'C'),
)


class DocumentForm(forms.Form):
    document = forms.FileField()
    categories = forms.MultipleChoiceField(choices=MOCK_CHOICES)


class CredentialsForm(forms.Form):
    """
    Contains:
            - informations collected from user when accepting files.
    """
    email = forms.EmailField()


DocumentsFormset = forms.formset_factory(DocumentForm, extra=1)
