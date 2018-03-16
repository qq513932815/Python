import pyaudio
import wave
import http.client, urllib.parse, json
import uuid
import urllib.request
import requests
import json
import os
import RPi.GPIO
import time
from xml.etree import ElementTree

def lu():
    CHUNK = 4096
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = "/var/python/bbb.wav"
    p = pyaudio.PyAudio()
    stream = p.open(
                    format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input_device_index = 2,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("* recording *")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording *")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
def byteify(input_data):
    # convert json to list
    if isinstance(input_data, dict):
        return {byteify(key): byteify(value) for key, value in input_data.iteritems()}
    elif isinstance(input_data, list):
        return [byteify(element) for element in input_data]
    else:
        return input_data
		
		
def get():
    apiKey = "xxxxxxxxxxxxxxxx"
    params = ""
    headers = {"Ocp-Apim-Subscription-Key": apiKey}
    AccessTokenHost = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"
    conn = http.client.HTTPSConnection(AccessTokenHost)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    conn.close()
    accesstoken = data.decode("UTF-8")
    print(accesstoken)
    return accesstoken
	
	
def read_in_chunks(file_object, chunk_size=1024):
    # post chunk encoding data
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data
def  ai(neirong):
    API_KEY = 'xxxxxxxxxxxxxxxx'
    url = "http://www.tuling123.com/openapi/api?key="+API_KEY+"&info="
    nei = neirong
    url = url+ urllib.request.quote(nei)
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data = response.read()
    data = data.decode('utf-8')
    print("Message")
    print(data)
    hjson = json.loads(data)
    return hjson['text']
def he(string):
    apiKey = "xxxxxxxxxxxxxxxx"
    params = ""
    headers = {"Ocp-Apim-Subscription-Key": apiKey}
    #AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
    AccessTokenHost = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"
    # Connect to server to get the Access Token
    print ("Connect to server to get the Access Token")
    conn = http.client.HTTPSConnection(AccessTokenHost)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()
    conn.close()

    accesstoken = data.decode("UTF-8")
    print ("Access Token: " + accesstoken)

    body = ElementTree.Element('speak', version='1.0')
    body.set('{http://www.w3.org/XML/1998/namespace}lang', 'zh-CN')
    voice = ElementTree.SubElement(body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'zh-CN')
    voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Female')
    voice.set('name', 'Microsoft Server Speech Text to Speech Voice (zh-CN, HuihuiRUS)')
    voice.text = string

    headers = {"Content-type": "application/ssml+xml", 
                            "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm", 
                            "Authorization": "Bearer " + accesstoken, 
                            "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA", 
                            "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960", 
                            "User-Agent": "TTSForPython"}
                            
    #Connect to server to synthesize the wave
    print ("\nConnect to server to synthesize the wave")
    conn = http.client.HTTPSConnection("speech.platform.bing.com")
    conn.request("POST", "/synthesize", ElementTree.tostring(body), headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()
    conn.close()

    fp = open("aaa.wav","wb")
    fp.write(data)
    fp.close()
    print("The synthesized wave length: %d" %(len(data)))
def bo():
    os.system('play /var/python/aaa.wav')

class MsSpeechRequest:
    def __init__(self, audiofile="bbb.wav", audioSamplerate=16000, clientid='', clientsecret='', locale='zh-CN', deviceOS='Rasbian'):
        if audiofile == None:
            print ('audio input wrong')
            return
        self._RequestUri = "https://speech.platform.bing.com/recognize"
        self._RequestUri += "?scenarios=smd"
        self._RequestUri += "&appid="+"D4D52672-91D7-4C74-8AD8-42B1D98141A5"
        self._RequestUri += "&locale="+locale
        self._RequestUri += "&device.os="+deviceOS
        self._RequestUri += "&version=3.0"
        self._RequestUri += "&format=json"
        self._RequestUri += "&instanceid="+"565D69FF-E928-4B7E-87DA-9A750B96D9E3"
        self._RequestUri += "&requestid="+str(uuid.uuid4())
        self._audioFile = audiofile
        self._audioSamplerate = audioSamplerate.__str__()
        self._token = get()
        # print self._token
        self._response = ''

    def post_request(self):
        headers = {}
        headers['Accept'] = 'application/json;text/xml'
        headers['Content-Type'] = 'audio/wav; codec=\"audio/pcm\"; samplerate='+self._audioSamplerate
        headers['Authorization'] = 'Bearer '+'%s' % self._token
        try:
            with open(self._audioFile,'rb') as f:
                r=requests.post(self._RequestUri, data=read_in_chunks(f), headers=headers, stream=True)
                print("Message")
                print (r)
                self._response = byteify(r.text)
                print("body")
                print(self._response)
        except Exception as e:
            print ('failed get request response. Details:%s',e.__str__())

    def returnResult(self):
        self.post_request()
        return self._response

btnR=21
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(btnR, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
try:
    while True:
            time.sleep(0.01)		
            if (RPi.GPIO.input(btnR) == 0):
                lu()
                requset = MsSpeechRequest()
                hjson = json.loads(requset.returnResult())
                if(hjson['header']['status']!='error'):
                    aineirong=ai(hjson['header']['name'])
                    he(aineirong)
                    bo()
except KeyboardInterrupt:
	pass

RPi.GPIO.cleanup()
