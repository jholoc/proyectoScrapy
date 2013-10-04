#-*-coding: utf-8 -*-

import codecs
from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata

urlscrap='http://ocw.jhsph.edu/index.cfm/go/viewCourse/course/Beyrer/coursePage/index/'

webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear
    
soup1 = BeautifulSoup(webpage1)
#print soup1
tiSoup = soup1.select("div.col1 li")#selecion de la pagina que contiene los titulos de las noticias
#print tiSoup
for i in tiSoup:
	print i.a.get('href')
	print i.text