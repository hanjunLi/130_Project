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

import json

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

def get_audio_from_str(string):
    tts = gTTS(text=string, lang='en', slow=False)
    return tts

def get_jason_response():
    # implementation through RPC
    pass

def make_tracks(jason_file, fs):
    data = json.load(jason_file)
    json_tracks = data['tracks']
    json_metadata = data['metadata']
    track_list = []
    for i in range(len(json_tracks)):
        audio = get_audio_from_str( json_tracks[str(i+1)]['content'] )
        with open('myaudio', 'w+b') as af:
            audio.write_to_fp(af)
            audio_url = fs.url(fs.save(af.name, af))
        track_list.append( track( json_tracks[str(i+1)]['id'], audio_url ) )
    return track_list
    
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

        if myfile.content_type.find('json') > -1:
            # json file with tracks
            with open(fs.path(filename), 'r') as json_file:
                template_dict['tracks'] = make_tracks(json_file, fs)
            
    return render(request, 'speaxapp/simple_upload.html', template_dict)
