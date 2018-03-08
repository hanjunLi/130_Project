from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World.")

# django util functions
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File

# import parser component, and run subprocess for local speach engine
import subprocess
import requests
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../../xml_parser'))
import xml_parser
import json
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

def get_audio_from_str(string):
    tts = gTTS(text=string, lang='en', slow=False)
    return tts

def get_json_response(pdfFile):
    # implementation through RPC
    url = "http://cloud.science-miner.com/grobid/api/processFulltextDocument"
    r = requests.post(url, files={'input' : ('tmp.pdf',
                                             pdfFile, 'application/pdf')})
    return json.loads(xml_parser.xml_parser('', r.text))

def make_tracks(data, fs, engine=1):
    # data = json.load(jason_file)
    json_tracks = data['tracks']
    json_metadata = data['metadata']
    track_list = []
    for i in range(len(json_tracks)):
        # decide to use local engine or google service
        if not json_tracks[str(i+1)]['content']:
            json_tracks[str(i+1)]['content'] = "no content"
        if engine == 1:
            audio = get_audio_from_str( json_tracks[str(i+1)]['content'] )            
            with open('myaudio', 'w+b') as af:
                audio.write_to_fp(af)
                audio_url = fs.url(fs.save(af.name, af))
        elif engine == 0:
            subprocess.call(["espeak", "-w tmp.wav", json_tracks[str(i+1)]['content']])
            with open('tmp.wav', 'rb') as af:
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
                template_dict['tracks'] = make_tracks(json.load(jason_file), fs, 1)

        if myfile.content_type.find('pdf') > -1:
            # pdf file
            with open(fs.path(filename), 'rb') as pdfFile:
                jsonData = get_json_response(pdfFile)
                template_dict['tracks'] = make_tracks(jsonData, fs, 1)
            
    return render(request, 'speaxapp/simple_upload.html', template_dict)
