#-*-coding: utf-8 -*-
import re,string,urlparse
import requests
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

def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )


tabla='CursosUctAcZa'

errores=[]
ObjBd = BDdatos()
datos=ObjBd.CursosOcwUctAcZa()

for cont,x in enumerate(datos):
    if cont<209 : 
        continue
    urlscrap=x[0]
    print '%s  %s'%(cont,urlscrap)  
    ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)#insertar en la bd Link
    ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type

    
    urlscrap=iriToUri(urlscrap)
    webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear 
    webpage1 = webpage1.replace('<p>','').replace('</p>','').replace('<td>','').replace('</td>','').replace('<br>','')
    soup1 = BeautifulSoup(webpage1)
    tiSoup = soup1.select("div.weblinks-linkview")#selecion de la pagina que contiene los titulos de las noticias
    banderaOer=False

    for i in tiSoup:
        tituloMenu=i.a.text.strip()
        urlMenu=unionurl('http://opencontent.uct.ac.za',i.a.get('href'))
        print urlMenu
        try:
            urlMenu2 = requests.get(urlMenu)
            print urlMenu2.url
        except Exception, e:
            print 'Ocurrio un ERROR'
            print '%s  %s'%(cont,urlscrap)
            print urlMenu
            errores.append('%s  %s ---> %s'%(cont,urlscrap,urlMenu))
            continue
            
        
        
        patron = re.compile("(\.(pdf|mp3|mp4|wmv|zip|tar|gz|html|htm|xls|xlsx|doc|docx|odt|ppt|pptx|XLS|DOCX|PPTX|jpg)$)") 
        busqueda=patron.search(urlMenu2.url)
        if busqueda!=None:
            ObjBd.insertar_datos_trip(urlscrap,'oer',urlMenu2.url,tabla)
            ObjBd.insertar_datos_trip(urlMenu2.url,'link',urlMenu2.url,tabla)
            
            extoer=extraerextoer(urlMenu2.url)
            ObjBd.insertar_datos_trip(urlMenu2.url,'rdf:type','oer',tabla)
            ObjBd.insertar_datos_trip(urlMenu2.url,'rdf:type',extoer,tabla)
            continue
        
        ObjBd.insertar_datos_trip(urlscrap,'menu',urlMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'link',urlMenu2.url,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'title',tituloMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'rdf:type','menu',tabla)
        nombreMenu=extraernombremenu(urlMenu)
        ObjBd.insertar_datos_trip(urlMenu,'rdf:type',nombreMenu,tabla)

        
        webpage2=urlopen(urlMenu2.url).read()
        soup2=BeautifulSoup(webpage2)
        htmlCurso = soup2
        


        ObjBd.insertar_datos_trip(urlMenu,'html',str(htmlCurso),tabla)


        if htmlCurso == []:
            continue

        hrefs= htmlCurso.find_all(href=re.compile("(\.(pdf|mp3|mp4|wmv|zip|tar|gz|html|htm|xls|xlsx|doc|docx|odt|ppt|pptx|XLS|DOCX|PPTX)$)"))
        
        if hrefs!=[]:
            banderaOer=True
            ObjBd.insertar_datos_trip(urlMenu,'existenOer','1',tabla)
        else:
            ObjBd.insertar_datos_trip(urlMenu,'existenOer','0',tabla)
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
            urlOer=unionurl(urlMenu2.url[0:len(urlMenu2.url)-1],href.get('href'))
           
            ObjBd.insertar_datos_trip(urlMenu,'oer',urlOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'title',descripOer ,tabla)
            ObjBd.insertar_datos_trip(urlOer,'description',textoOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'html',str(htmlOer),tabla)

            extoer=extraerextoer(urlOer)
            ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
            ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)


    if banderaOer==True:
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','1',tabla)
    else:
        print 'NO HAY OERS'
        print urlscrap
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)
for error in errores:
    print error