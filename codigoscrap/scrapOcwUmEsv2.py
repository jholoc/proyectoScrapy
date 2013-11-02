#-*-coding: utf-8 -*-
import re,string
from bs4 import *
from urllib import urlopen
from bd import *
from scrapUniversidades import *
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

Scrapear = Scrap()
url='http://ocw.uv.es/artes-y-humanidades/narrativa-breve-de-los-estados-unidos'
tabla='Prueba'
Scrapear.ScrapUniverdidades(url,tabla)