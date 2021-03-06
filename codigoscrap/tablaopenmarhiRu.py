#-*-coding: utf-8 -*-
import re,string
from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def eliminasignos( text ):
    return re.sub('[%s]' % re.escape(string.punctuation), '', text)

def removersignos(text):
    signos=(',','.',';','+','{','}','[',']','(',')','^','~','#')
    for sig in signos:
        text=text.replace(sig,"")
    return text

def unionurl(urlpag,urloer):
    if 'http://' in urloer:
        return urloer
    else:
        list1= urlpag.split('/')
        list2= urloer.split('/')
        list1.extend([element for element in list2 if element not in list1])
        union= '/'.join(list1)
        return union
def extraernombremenu(urlmenu):
    url=urlmenu.split('/')
    return url[len(url)-1]

def extraerextoer(urlmenu):
    url=urlmenu.split('.')
    return url[len(url)-1]


tabla='tablaopenmarhiru'


ObjBd = BDdatos()
datos=ObjBd.CursosOcwOpenmarhiRu()

for cont,x in enumerate(datos):
    if cont<0 : 

        continue
    urlscrap=x[0]
    print '%s  %s'%(cont,urlscrap)  
    ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)#insertar en la bd Link
    ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type

    webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear 
    webpage1 = webpage1.replace('<p>','').replace('</p>','').replace('<td>','').replace('</td>','')
    soup1 = BeautifulSoup(webpage1)
    tiSoup = soup1.select("div.left_menu_item")#selecion de la pagina que contiene los titulos de las noticias
    banderaOer=False

    for i in tiSoup:
        tituloMenu=i.a.text.strip()
        urlMenu=unionurl("http://www.open-marhi.ru",i.a.get('href'))
        
        ObjBd.insertar_datos_trip(urlscrap,'menu',urlMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'link',urlMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'title',tituloMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'rdf:type','menu',tabla)
        nombreMenu=extraernombremenu(urlMenu)
        ObjBd.insertar_datos_trip(urlMenu,'rdf:type',nombreMenu,tabla)
        
        try:
            ObjBd.insertar_datos(urlscrap,urlMenu,tituloMenu,'','','tablaopenmarhiru')
        except Exception, e:
            print e
            continue
        
        webpage2=urlopen(urlMenu).read()
        soup2=BeautifulSoup(webpage2)
        htmlCurso = soup2.select('#content')#html del curso
        


        ObjBd.insertar_datos_trip(urlMenu,'html',str(htmlCurso),tabla)


        if htmlCurso == []:
            continue
        hrefs= htmlCurso[0].find_all(href=re.compile("(\.(pdf|mp3|mp4|zip|tar|gz|html|htm|xls|xlsx|doc|docx|odt|ppt|pptx)$)"))
        
        if hrefs!=[]:
            banderaOer=True
            ObjBd.insertar_datos_trip(urlMenu,'existenOer','1',tabla)
    
        for href in hrefs:
            aux=href.previous_element
            while len(str(aux).replace(' ',''))<=3 or str(aux)[0]=='<':
                if str(aux)[0]=='<':
                    if str(aux)[1]=='a':
                        break
                    else:
                        if str(aux)[1]=='t' or str(aux)[1]=='i' or str(aux)[1]=='p' or str(aux)[1]=='s' or str(aux)[1]=='e':
                            aux=aux.previous_element
                        else:
                            break
                else:
                    aux=aux.previous_element

            if str(aux)[0]=='<':
                if str(aux)[1]=='a':
                    pass
                else:
                    htmlOer=aux.parent # html del oer
                    descripOer=removersignos(aux.text).strip()

            else:
                htmlOer=aux.parent
                descripOer=removersignos(aux).strip()

            textoOer=href.text
            urlOer=unionurl("http://www.open-marhi.ru",href.get('href'))


            ObjBd.insertar_datos_trip(urlMenu,'oer',urlOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'title',descripOer ,tabla)
            ObjBd.insertar_datos_trip(urlOer,'description',textoOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'html',str(htmlOer),tabla)

            extoer=extraerextoer(urlOer)
            ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
            ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)
            try:
                ObjBd.insertar_datos(urlscrap,urlMenu,tituloMenu,urlOer,descripOer,'tablaopenmarhiru')
            except Exception, e:
                print e
                continue


    if banderaOer==True:
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','1',tabla)
    else:
        print 'NO HAY OERS'
        print urlscrap
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)