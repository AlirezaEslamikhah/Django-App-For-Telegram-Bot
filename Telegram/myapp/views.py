from django.shortcuts import render
# from rest_framework.generics import GenericAPIView
# Create your views here.
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

