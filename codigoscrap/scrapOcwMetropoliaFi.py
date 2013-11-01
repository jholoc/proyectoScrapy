#-*-coding: utf-8 -*-
#falta view, en esta paguina hay varios tipos de oer
import re,string,requests
from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata
import sys
import urllib
reload(sys)
sys.setdefaultencoding("utf-8")


def eliminasignos( text ):
    text=eliminaNumeros(text)
    return re.sub('[%s]' % re.escape(string.punctuation), '', text)
def eliminaNumeros( text ):
    return re.sub('[%s]' % re.escape(string.digits), '', text)

def removersignos(text):
    signos=(',','.',';','+','{','}','[',']','(',')','^','~','#')
    for sig in signos:
        text=text.replace(sig,"")
    return text

def unionurl(urlpag,urloer):
    if 'http://' in urloer:
        return urloer
    else:
        list1= urlpag.strip().split('/')
        list2= urloer.strip().split('/')
        list1.extend([element for element in list2 if element not in list1])
        union= '/'.join(list1)
        return union
def extraernombremenu(urlmenu):
    url=urlmenu.split('/')
    return url[len(url)-1]

def extraerextoer(urlmenu):
    url=urlmenu.split('.')
    return url[len(url)-1]
def identificarOer(url):
    if identificarOer2(url)=='0':
        #print 'if'
        url=requests.get(url).url
        return identificarOer2(url)
    else:
        #print 'else'
        return identificarOer2(url)

def identificarOer2(url):
    patron = re.compile("(\.(pdf|mp3|mp4|wmv|zip|rar|tar|gz|htm|xls|xlsx|doc|docx|odt|ppt|pptx|XLS|DOCX|PPTX|jpg)$)")
    if "http://www.youtube.com/watch" in url:
        return'video Youtube'
    busqueda=patron.search(url)
    try:
        if busqueda==None:  
            urlOpen=urllib.urlopen(url)
            infoUrl=urlOpen.info()['Content-Type']
            #print infoUrl
            if infoUrl=='application/pdf':
                return 'pdf'
            elif infoUrl=='application/zip':
                return 'zip'
            elif infoUrl=='application/octet-stream':
                return 'rar'
            elif infoUrl=='application/msword':
                return 'dot'
            elif infoUrl=='application/pdf;charset=UTF-8':
                return 'pdf'
            else:
                return '0'
        else:
            return extraerextoer(url)
    except Exception, e:
                return '0'
def EncuentraDescripcion(aux):
    while len(eliminasignos(str(aux).replace(' ','').strip()))<=3 or str(aux)[0]=='<':
        if str(aux)[0]=='<':
            if str(aux)[1]=='a':
                aux=aux.previous_element
                #break
            else:
                if str(aux)[1]=='t' or str(aux)[1]=='i' or str(aux)[1]=='p' or str(aux)[1]=='s' or str(aux)[1]=='e' or (str(aux)[1]=='t' and str(aux)[2]=='d'):
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
            descripOer=removersignos(aux.text).strip()#aux.text
            #print '    %s'%descripOer

    else:
        htmlOer=aux.parent
        descripOer=removersignos(aux).strip()#aux
        #print '   %s'%descripOer

    return [descripOer,htmlOer]



tabla='CursosMetropoliaFi'

ObjBd = BDdatos()
#ObjBd.crearTabla(tabla)
#sys.exit()

datos=ObjBd.CursosOcwMetropoliaFi()


for cont,x in enumerate(datos):
    urlscrap=x[0]
    print '%s  %s'%(cont,urlscrap)
    if cont<0:
        continue
    
    ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)#insertar en la bd Link
    ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type

    webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear 
    webpage1 = webpage1.replace('<p>','').replace('</p>','').replace('<br>','')
    soup1 = BeautifulSoup(webpage1)

    banderaOer=False
    htmlCurso = soup1.select('#main-content')#html del curso
    if htmlCurso==[]:
        continue

    ObjBd.insertar_datos_trip(urlscrap,'html',str(htmlCurso[0]),tabla)

    hrefs= htmlCurso[0].find_all('a', href=True)

    if hrefs!=[]:
        #print 'Si hay oer'
        banderaOer=True
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','1',tabla)
    else:
        pass
        #print 'No hay Oers'
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)

    for href in hrefs:

        urlOer=unionurl('https://wiki.metropolia.fi',href.get('href'))
        try:
            extoer=identificarOer(urlOer)
        except Exception, e:
            continue
        
        if extoer=='0':
            continue
        
        print urlOer
        decripOer=EncuentraDescripcion(href.previous_element)
        textoOer=href.text
        descripOer=decripOer[0]
        htmlOer=decripOer[1]
        
        ObjBd.insertar_datos_trip(urlscrap,'oer',urlOer,tabla)
        ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
        ObjBd.insertar_datos_trip(urlOer,'title',descripOer ,tabla)
        ObjBd.insertar_datos_trip(urlOer,'description',textoOer,tabla)
        ObjBd.insertar_datos_trip(urlOer,'html',str(htmlOer),tabla)
        ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
        ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)


if banderaOer==True:
    pass
    #print 'SI HAY OERS'
    ObjBd.insertar_datos_trip(urlscrap,'existenOer','1',tabla)
else:
    print 'NO HAY OERS'
    print urlscrap
    ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)