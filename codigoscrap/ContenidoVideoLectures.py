# -*- coding: utf-8 -*-
#import re,string,requests
#from bs4 import *
#from urllib import urlopen
#from bd import *
import unicodedata
import sys
import urllib
#import urllib2
#from urlparse import urljoin
#reload(sys)

urlscrap='http://videolectures.net/metaforum2011_eulanguage_debate/'
print (urlscrap)

import urllib.request
response = urllib.request.urlopen('http://python.org/')
html = response.read()
print(html)

"""
try:
    webpage1 = urllib2.urlopen(urlscrap).read() #lectura de la pagina a scrapear 
    webpage1 = requests.get(urlscrap).text
    webpage1 = urllib.urlopen(urlscrap)
    nose=webpage1.read()
    #print nose
    webpage1 = webpage1.replace('<p>','').replace('</p>','').replace('<br>','')
    soup = BeautifulSoup(webpage1)
    #print soup
    soup1 = soup.select('#vl_desc')
    soup2 = soup.select('#hint_list')
    Datos = soup1[0].select('div.lec_data > span')
    Categ = soup1[0].select('#categories > ul > li > span > a')# "table.upv_lista"  selecion de la pagina que contiene los titulos de las noticias
    VidRela = soup2[0].select('a')
    print (Categ)
    print (Datos[5])
    print (Datos[5].next_element.next_element)
    print (Datos[5].next_element.next_element.next_element)
    print (Datos[5].next_element.next_element.next_element.next_element)
    print (VidRela)

except Exception, e:
    print e
    continuar=False"""