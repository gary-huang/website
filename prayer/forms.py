from django import forms


class PrayerRequestForm(forms.Form):
    VISIBILITY_CHOICES = [
        ("", "Only you"),
        ("member", "Only Crossroads members"),
        ("prayer_team", "Only Crossroads prayer team members"),
    ]
    body = forms.CharField(label="Prayer request", max_length=8192, widget=forms.Textarea(attrs={
        "rows": 3,
        "placeholder": "your prayer request or praise report",
    }))
    body_visibility = forms.ChoiceField(choices=VISIBILITY_CHOICES, label="Who can see your submission", initial="member")
    provided_name = forms.CharField(label="Name", max_length=48, required=False)
    provided_name.widget.attrs.update({
        "rows": 1,
        "placeholder": "Name (optional)",
    })

