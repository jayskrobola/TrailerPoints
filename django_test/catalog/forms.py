from django import forms

class CreateNewCatalog(forms.Form):
    name = forms.CharField(label='Catalog Name', max_length=200)

class CreateNewProduct(forms.Form):
    link = forms.CharField(label='Product Link', max_length=500)