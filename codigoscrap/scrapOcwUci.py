#-*-coding: utf-8 -*-           
import re,string
from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

tabla='CursosUci'


ObjBd = BDdatos()
datos=ObjBd.CursosOcwUci()
urlscrap='http://ocw.uci.edu/lectures/lecture.aspx?id=499'

for cont,x in enumerate(datos):
    if cont<100:#http://ocw.uci.edu/lectures/lecture.aspx?id=156
        continue
    urlscrap=x[0]
    print '%s  %s'%(cont,urlscrap)  
    ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)#insertar en la bd Link
    ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type

    webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear 
    soup1 = BeautifulSoup(webpage1)
    htmlcurso=soup1.select('div.columnleft_nomiddle')
    ViSoup = soup1.select('iframe')

    ObjBd.insertar_datos_trip(urlscrap,'html',str(htmlcurso),tabla)


    if ViSoup != []:
    	urlvi=ViSoup[0].get('src')
    	if urlvi.find('embed/')<0:
    		ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)
    		continue
        urlvi=urlvi.replace('embed/','watch?v=')

        webpage2=urlopen(urlvi).read()
        soup2=BeautifulSoup(webpage2)
        titulosoup = soup2.select('#eow-title')
        titulo=titulosoup[0].text
        descipcionsoup= soup2.select('#eow-description')
        descipcion= descipcionsoup[0].text

        ObjBd.insertar_datos_trip(urlscrap,'oer',urlvi,tabla)
        ObjBd.insertar_datos_trip(urlvi,'link',urlvi,tabla)
        ObjBd.insertar_datos_trip(urlvi,'title',titulo ,tabla)
        ObjBd.insertar_datos_trip(urlvi,'description',descipcion,tabla)
        ObjBd.insertar_datos_trip(urlvi,'html',str(webpage2),tabla)

        ObjBd.insertar_datos_trip(urlvi,'rdf:type','oer',tabla)
        ObjBd.insertar_datos_trip(urlvi,'rdf:type','video',tabla)

        print urlvi
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','1',tabla)
    else:
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)
