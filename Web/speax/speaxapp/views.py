from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World.")

# Create your views here.
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'speaxapp/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'speaxapp/simple_upload.html')
