from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    text = "hello all!"
    return HttpResponse(text)

    # attempt at pulling in whole text file from database!
    #gal_war_eng = ""
    #for t in Text.objects.all():
    #    gal_war_eng += t.text_field
    #    gal_war_eng += '\n'
    #    #return HttpResponse(t.text_field)
    #response_text = "<pre>" + gal_war_eng + "</pre>"
    #return HttpResponse(response_text) #gal_war_eng) #, content_type='text/plain')
    #return HttpResponse("Hello, world!!! \nIt's me, Palimpsest ;)")
    #arr = gal_war_eng.split('\n')
    #arr_len = len(arr)
    #return HttpResponse(arr_len)
