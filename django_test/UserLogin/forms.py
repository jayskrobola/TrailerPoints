from django import forms

class CreateNewCatalog(forms.Form):
    name = forms.CharField(label='Catalog Name', max_length=200)


paymentmethod= [
    ('Credit','Credit'),
    ('Debit','Debit'),
    ('Visa','Visa')
    ]

class CHOICES(forms.Form):
    paymentmethod=forms.CharField(widget=forms.RadioSelect(choices=paymentmethod))
