
from django import forms
from django.forms import ModelForm
from models import Author, Book, Contact

from django.core.exceptions import NON_FIELD_ERRORS


from django.forms.models import inlineformset_factory

from models import (
    Contact,
    Address,
)

# inlineformset_factory creates a Class from a parent model (Contact)
# to a child model (Address)
ContactAddressFormSet = inlineformset_factory(
    Contact,
    Address,
    fields='__all__'
)
#BookFormSet = inlineformset_factory(Author, Book, fields=('title',))


class ContactForm(forms.ModelForm):

    confirm_email = forms.EmailField(
        label="Confirm email",
        required=True,
    )

    class Meta:
        model = Contact
        fields='__all__'

    def __init__(self, *args, **kwargs):

        if kwargs.get('instance'):
            email = kwargs['instance'].email
            kwargs.setdefault('initial', {})['confirm_email'] = email

        return super(ContactForm, self).__init__(*args, **kwargs)

    #custom validation
    def clean(self):

        if (self.cleaned_data.get('email') !=
            self.cleaned_data.get('confirm_email')):

            raise ValidationError(
                "Email addresses must match."
            )

        return self.cleaned_data

'''
class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

'''

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']
  

class ArticleForm(ModelForm):

    class Meta:
        
        model = Author
        fields = '__all__'
        #exclude = ['title']

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }



#Separate EXAMPLE
class PostForm(forms.Form):
    content = forms.CharField(max_length=256)
    created_at = forms.DateTimeField()


