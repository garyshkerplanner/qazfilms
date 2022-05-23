from dataclasses import field
from xml.etree.ElementTree import Comment
from django import forms


from .models import Comments, RatingStars, Ratings

class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStars.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Ratings
        fields = ("star",)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ("text", "user", "movie")
