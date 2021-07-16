from django import forms
from .models import Comment

class EmailPostForm(forms.Form):

    """ Creating post form for email so that we can send post. Used forms.Form - allows sending emails, in static way"""

    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.CharField()
    comments = forms.CharField(required=False, widget=forms.Textarea) #default widget is input, but we can overwrite it with textarea


class CommentForm(forms.ModelForm):

    """ Creating Comment form for commening posts.
    Here w use ModelForm, as it allows to dinamically create form based on Comment model"""

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

