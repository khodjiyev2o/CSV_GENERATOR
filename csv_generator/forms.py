from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import DataSchema, Column
from .services.data_types import *
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))




class DataSchemaForm(forms.ModelForm):
    class Meta:
        model = DataSchema
        fields = ('name', 'column_separator', 'string_character')

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                

class SchemaColumnForm(forms.ModelForm):

    class Meta:
        model = Column
        fields = ('column_name', 'data_type', 'order')
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
    
               

class CombinedForm(SchemaColumnForm, DataSchemaForm):
    pass