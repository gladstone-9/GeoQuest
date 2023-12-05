from django.forms import ModelForm, inlineformset_factory, HiddenInput, Textarea, Select
from .models import Quest, Location
from django import forms


class QuestForm(ModelForm):
    class Meta:
        model = Quest
        fields = ["title", "cache_type"]

class QuestUpdateForm(ModelForm):
    class Meta:
        model = Quest
        fields = ['feedback','status']
        widgets = {
            'feedback': Textarea(),
            'status': HiddenInput(),
        }

class LikesForm(ModelForm):
    class Meta:
        model = Quest
        fields = ["likes"]

class DifficultyForm(ModelForm):
    class Meta:
        model = Quest
        fields = ["difficulty", "num_ratings", "ratings_total"]
        widgets = {
            'difficulty': Select(choices=[(i, i) for i in range(1, 6)]),
            'num_ratings': HiddenInput(),
            'ratings_total': HiddenInput(),
        }

class GuessForm(ModelForm):
    class Meta:
        model = Location
        fields = ["answer"]


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ["title", "clue", "lat", "long", "description", "answer"]
        widgets = {
            'lat': forms.TextInput(attrs={'readonly': 'readonly'}),
            'long': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


ChoiceFormSet = inlineformset_factory(Quest, Location, form=LocationForm, extra=1)