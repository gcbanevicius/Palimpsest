#from annoying.decorators import render_to
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader, Context, Template
from django.views.generic import TemplateView


def home(request):
	 return render(request, 'homepage.html')

def about(request):
	 return render(request, 'about.html')

def contact(request):
	 	 return render(request, 'contact.html')
