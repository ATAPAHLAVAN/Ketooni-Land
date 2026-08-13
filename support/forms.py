from django import forms

class ChatForm(forms.Form):
    message = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "پیام خود را بنویس..."
            }
        )
    )