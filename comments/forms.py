from django import forms


class CommentForm(forms.Form):
    body = forms.CharField(label="Comment", max_length=8192, widget=forms.Textarea(attrs={
        "rows": 3,
        "placeholder": "Comment"
    }))
