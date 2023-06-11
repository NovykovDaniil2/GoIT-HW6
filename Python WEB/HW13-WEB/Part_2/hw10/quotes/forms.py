from django.forms import ModelForm, CharField, TextInput, DateField
from .models import Tag, Author, Quote


class TagForm(ModelForm):
    name = CharField(min_length=4, max_length=32, required=True, widget=TextInput(attrs={'placeholder': 'Tag'}))

    class Meta:
        model = Tag
        fields = ['name']

    
class AuthorForm(ModelForm):
    fullname = CharField(required=True, widget=TextInput(attrs={'placeholder': 'Fullname'}))
    born_date = DateField(widget=TextInput(attrs={'placeholder': 'Born date (year-month-day)'}))
    born_location = CharField(widget=TextInput(attrs={'placeholder': 'Born location'}))
    biography = CharField(widget=TextInput(attrs={'placeholder': 'Biography'}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'biography']


class QuoteForm(ModelForm):
    quote = CharField(min_length = 8, max_length = 128, required=True, widget=TextInput(attrs={'placeholder': 'Quote'}))

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['tags', 'author']