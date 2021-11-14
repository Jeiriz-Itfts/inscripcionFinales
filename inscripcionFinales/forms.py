from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label='juan.eiriz@alu.ifts18.edu.ar')