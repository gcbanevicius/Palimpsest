from django.db import models
from django import forms

# Create your models here.

#class Text(models.Model):
#    text_field = models.CharField(max_length=200)

class QueryForm(forms.Form):
    range = forms.CharField(max_length=20)

class Comment(models.Model):
    #path = models.CharField(max_length=20) #DecimalField(decimal_places=10, max_digits=20)
    book = models.IntegerField()
    line = models.IntegerField()    
    public = models.BooleanField()
    user_id = models.IntegerField()
    text_name = models.CharField(max_length=255)
    comment_text = models.TextField()
    anonymous = models.BooleanField()
