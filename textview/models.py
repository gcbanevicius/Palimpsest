from django.db import models
from django import forms

# Create your models here.

class Text(models.Model):
    text_field = models.CharField(max_length=200)

class QueryForm(forms.Form):
    range = forms.CharField(max_length=20)
