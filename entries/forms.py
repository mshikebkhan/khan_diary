from django import forms

from .models import Entry


# Mood choice
moods = [
    ('great', "Great mood"),
    ('good', "Good mood"),
    ('usual', "Usual mood"),
    ('bad', "Bad mood"),
    ('terrible', "Terrible mood")
]


class EntryForm(forms.ModelForm):
    """ New entry form (using bulma inputs) """
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'textarea is-medium is-rounded is-success', 'rows': "7",
               'placeholder': "Tell me what happen today", 'autocomplete': 'off', 'autofocus': '""'})
    , max_length=750)

    mood = forms.ChoiceField(choices=moods)


    class Meta():
        model = Entry
        fields = ['content', 'mood']


