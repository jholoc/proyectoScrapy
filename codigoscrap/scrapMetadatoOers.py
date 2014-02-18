import re,string,requests
from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata
import sys
import urllib
import urllib2

from hachoir_core.error import HachoirError
from hachoir_core.stream import InputIOStream
from hachoir_parser import guessParser
from hachoir_metadata import extractMetadata


def metadata_for_filelike(filelike):
    try:
        filelike.seek(0)
    except (AttributeError, IOError):
        return None

    stream = InputIOStream(filelike, None, tags=[])
    parser = guessParser(stream)

    if not parser:
        return None

    try:
        metadata = extractMetadata(parser)
    except HachoirError:
        return None

    return metadata

print metadata_for_filelike('http://ocw.unican.es/ensenanzas-tecnicas/arquitectura-e-ingenieria-de-computadores/materiales/11_Final.pdf')

request = urllib2.Request("http://ocw.unican.es/ensenanzas-tecnicas/arquitectura-e-ingenieria-de-computadores/materiales/11_Final.pdf")
response = urllib2.urlopen(request)
print(response.info().items())

r = requests.get('http://ocw.unican.es/ensenanzas-tecnicas/arquitectura-e-ingenieria-de-computadores/materiales/11_Final.pdf')
r.status_code
print r.headers

url='http://ocw.unican.es/ensenanzas-tecnicas/arquitectura-e-ingenieria-de-computadores/materiales/11_Final.pdf'
urlOpen=urllib.urlopen(url)
infoUrl=urlOpen.info()
print infoUrl

response = urllib2.urlopen(url)
headers = response.info()
print headers

remotefile = urllib2.urlopen('http://ocw.unican.es/ensenanzas-tecnicas/arquitectura-e-ingenieria-de-computadores/materiales/11_Final.pdf')
print remotefile.info()