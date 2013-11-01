#-*-coding: utf-8 -*-
import re,string,requests
from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata
import sys
import urllib
reload(sys)
sys.setdefaultencoding("utf-8")

tabla='CursosUniversia'

ObjBd = BDdatos()
#ObjBd.crearTabla(tabla)
#sys.exit()

datos=ObjBd.CursosOcwUniversia()

for cont,x in enumerate(datos):
    urlscrap=x[0]
    print '%s  %s'%(cont,urlscrap)
    if cont<201:
    	continue
    try:
        webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear 
        soup1 = BeautifulSoup(webpage1)
        urlSoup = soup1.select("h3 > strong")#selecion de la pagina que contiene los titulos de las noticias
        for i in urlSoup:
            tituloMenu=i.a.text.strip()
            urlOcw=i.a.get('href')
            #print urlOcw
            univerUrl= urlOcw.split('/')[2]
            #print univerUrl
            ObjBd.insertar_datos_trip(urlscrap,'link',urlOcw,tabla)#insertar en la bd Link
            ObjBd.insertar_datos_trip(urlscrap,'universidad',univerUrl,tabla)#insertar en la bd Link

    except Exception, e:
        print 'error en %s'%urlscrap
        ObjBd.insertar_datos_trip(urlscrap,'link','Error al Abrirla',tabla)#insertar en la bd Link
        continue
