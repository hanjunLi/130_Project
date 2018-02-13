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

class track:
    def __init__(self, name="", path=""):
        self.name = name
        self.path = path
        

def get_audio_from_text(text_file):
    # real implementation may use other speech engine
    # temporarily: use gTTS over internet
    text_buffer = text_file.read()
    tts = gTTS(text=text_buffer, lang='en', slow=False)
    return tts

def get_jason_response():
    # real implementation through RPC
    # temporarily: read from file
    pass

def make_tracks(jason_data):
    
    pass


def simple_upload(request):
    template_dict = {};

    
    if request.method == 'POST' and 'myfile' in request.FILES:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        template_dict['uploaded_file_url'] = uploaded_file_url
        template_dict['file_type'] = myfile.content_type
        if myfile.content_type == "text/plain" and not myfile.multiple_chunks():
            # small text/plain type file
            with open(fs.path(filename), 'r') as text:
                audio = get_audio_from_text(text)
                
            with open('myaudio', 'w+b') as af:
                audio.write_to_fp(af)
                audio_url = fs.url(fs.save(af.name, af))

            template_dict['tracks'] = [track("uploaded_text", audio_url)]

    return render(request, 'speaxapp/simple_upload.html', template_dict)
