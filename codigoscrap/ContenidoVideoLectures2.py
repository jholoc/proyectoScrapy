# -*- coding: utf-8 -*-
import re,string,requests
from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata
import sys
import urllib
import urllib2
from urlparse import urljoin
reload(sys)

def unionurl(urlpag,urloer):
    if 'http://' in urloer or 'https://' in urloer:
        if 'view.php?id=' in urloer:    
            return urloer+'&redirect=1'
        return urloer
    else:
        union=urljoin(urlpag,urloer)
        return union

ObjBd = BDdatos()
tabla='DatosVideoLectures'
datos=ObjBd.consulta('''SELECT sujeto FROM ConsortiumCursos080114 where predicado="urlCourseOCWC" and sujeto like "http://videolectures.net/%" ;''')
#ObjBd.crearTablalord(tabla)
#sys.exit()
for cont,urlvideoslectu in enumerate(datos):
    urlscrap=urlvideoslectu[0]
    if cont<0:
        continue
    #urlscrap='http://videolectures.net/metaforum2011_eulanguage_debate/'
    print cont
    print '%s - %s - %s'%(urlscrap,'url',urlscrap)
    ObjBd.insertar_datos_trip_lord(urlscrap,'url',urlscrap,tabla)
    try:
        webpage1 = urllib2.urlopen(urlscrap).read() #lectura de la pagina a scrapear 
        webpage1 = webpage1.replace('<p>','').replace('</p>','').replace('<br>','')
        soup = BeautifulSoup(webpage1)
        soup1 = soup.select('#vl_desc')
        #soup2 = soup.select('#hint_list')
        Titulo= soup1[0].select('h2')
        Datos = soup1[0].select('div.lec_data > span')
        Categ = soup1[0].select('#categories > ul > li > span > a')# "table.upv_lista"  selecion de la pagina que contiene los titulos de las noticias
        #VidRela = soup2[0].select('a')
        titulo=Titulo[0].text
        print '%s - %s - %s'%(urlscrap,'titulo',titulo)
        ObjBd.insertar_datos_trip_lord(urlscrap,'titulo',titulo,tabla)
        for Dato in Datos:
            tipo= (Dato).text
            if str(Dato.next_element.next_element.encode('utf-8'))[0:2]=='<a':
            	nombre= (Dato.next_element.next_element.text)
            	link_incom_autor=(Dato.next_element.next_element.get('href'))
            	link_autor= unionurl(urlscrap,link_incom_autor)
            	equipo= (Dato.next_element.next_element.next_element.next_element.encode('utf-8')).replace(',',"").strip()

            	print '%s - %s - %s'%(urlscrap,tipo,nombre+', '+equipo)
                print '%s - %s - %s'%(urlscrap,'link'+tipo,link_autor)

                ObjBd.insertar_datos_trip_lord(urlscrap,tipo,nombre+', '+equipo,tabla)
                ObjBd.insertar_datos_trip_lord(urlscrap,'link'+tipo,link_autor,tabla)
            else:
            	contenido= (Dato.next_element.next_element).strip()
            	print '%s - %s - %s'%(urlscrap,tipo,contenido)

                ObjBd.insertar_datos_trip_lord(urlscrap,tipo,contenido,tabla)

        #print('Categorias:')
        for catego in Categ:
            cat = catego.text
            link_cate_incom=catego.get('href')
            link_cate= unionurl(urlscrap,link_cate_incom)
            print '%s - %s - %s'%(urlscrap,'categoria:',cat)
            print '%s - %s - %s'%(urlscrap,'linkcategoria:',link_cate)

            ObjBd.insertar_datos_trip_lord(urlscrap,'categoria:',cat,tabla)
            ObjBd.insertar_datos_trip_lord(urlscrap,'linkcategoria:',link_cate,tabla)

        #print (VidRela)

    except Exception, e:
        print e
