from django import forms

class JSONImportForm(forms.Form):
    json_file = forms.FileField(label="JSON file")