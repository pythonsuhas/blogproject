from django import forms

class EmailSendForm(forms.Form):
    name=forms.CharField()
    email=forms.CharField()
    to=forms.CharField()
    comments=forms.CharField(required=False,widget=forms.Textarea)

from testapp.models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')    
