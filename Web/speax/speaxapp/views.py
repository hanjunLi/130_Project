from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World.")

# Create your views here.
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File

# gtts or other speech engine
from gtts import gTTS

def get_audio_from_text(text_file):
    text_buffer = text_file.read()
    tts = gTTS(text=text_buffer, lang='en', slow=False)
    return tts


def simple_upload(request):
    if request.method == 'POST' and 'myfile' in request.FILES:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        if myfile.content_type == "text/plain" and not myfile.multiple_chunks():
            # small text/plain type file
            with open(fs.path(filename), 'r') as text:
                audio = get_audio_from_text(text)
                
            with open('myaudio', 'w+b') as af:
                audio.write_to_fp(af)
                audio_url = fs.url(fs.save(af.name, af))
                
            return render(request, 'speaxapp/simple_upload.html', {
                'uploaded_file_url': uploaded_file_url,
                'file_type' : myfile.content_type,
                'audio_path' : audio_url
            })

        else:
            return render(request, 'speaxapp/simple_upload.html', {
                'uploaded_file_url': uploaded_file_url,
                'file_type' : myfile.content_type
            })
    return render(request, 'speaxapp/simple_upload.html')
