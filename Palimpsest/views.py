from annoying.decorators import render_to
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader, Context, Template
from django.views.generic import TemplateView


def home(request):
	return HttpResponse(render_to_response('homepage.html'))
