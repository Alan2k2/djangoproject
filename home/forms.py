from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=254)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(max_length=5000, widget=forms.Textarea)
