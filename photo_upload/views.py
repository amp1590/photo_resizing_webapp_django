from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files import File #I added
#from . import form
from .forms import UploadPhotoForm
from django.core.mail import send_mail #for contactForm class
from django.core.mail import EmailMessage #for sending email with attachment
from django.core.files.storage import FileSystemStorage #for storing uploaded files in media

#from .test import *
from .PhotoResize import *

#import subprocess
from subprocess import run, PIPE #For calling external python script
import sys


# Create your views here.

def photo_upload(request):
    #return HttpResponse("Hello Python!!")
    # if this is a POST request we need to process the form data
    context = {}
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UploadPhotoForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            
            # process the data in form.cleaned_data as required
            # ...
            #1st parameter - input file
            # Uploaded file saving
            title=form.cleaned_data.get("title")

            #Deleting the all the media files before uploading:
            dir = './media/'
            for file in os.scandir(dir):
                os.remove(file.path)

            #For saving multiple files:
            for f in request.FILES.getlist("img"):
                #print(f.name)
                fs = FileSystemStorage()
                img_name = fs.save(f.name, f)
                img_path = fs.url(img_name)
                img_path = '.'+img_path
                #print(img_path)

            """ 
            #For saving single file:  
            uploaded_img=request.FILES['img']
            print(uploaded_img.name)
            fs = FileSystemStorage()
            img_name = fs.save(uploaded_img.name, uploaded_img)
            img_path = fs.url(img_name)
            img_path = '.'+img_path
            print(img_path)
            """
            #recipient = form.cleaned_data['recipient'] #for email
            main()

            return render(request, 'resize_result/resize_result.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadPhotoForm()
    context['form']= form
    return render(request, 'photo_upload/photo_upload.html', context)

def download_zip_file(request):
    zip_file = open('./resize_result/static/resized_photos.zip', 'rb') #Here "Putting 'r' instead of 'rb' gave UnicodeDecodeError initially
    response = HttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'resized_photos.zip'
    return response
    #return FileResponse(zip_file)
    