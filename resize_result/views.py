from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def resize_result(request):
    #return HttpResponse("Hello Python!!")
    return render(request, 'resize_result/resize_result.html')

