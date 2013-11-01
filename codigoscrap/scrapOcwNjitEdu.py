#-*-coding: utf-8-sig -*-
import requests
import re,string
from bs4 import *
from urllib import urlopen
from bd import *
#import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
def removersignos(text):
    signos=(',','.',';','+','{','}','[',']','(',')','^','~','#')
    for sig in signos:
        text=text.replace(sig,"")
    return text


def unionurl(urlpag,urloer):
    if 'http://' in urloer and urloer[0]=='h':
        return urloer
    else:
        list1= urlpag.split('/')
        list2= urloer.split('/')
        list1.extend([element for element in list2 if element not in list1])
        union= '/'.join(list1)
        return str(union)
def extraerextoer(url):
    url=url.split('.')
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
            else:
                return '0'
        else:
            return extraerextoer(url)
    except Exception, e:
                return '0'

tabla='CursosNjitEdu'


ObjBd = BDdatos()
datos=ObjBd.CursosOcwNjitEdu()
urlscrap='http://oer.avu.org/handle/123456789/139'


for cont,x in enumerate(datos):
    if cont<0:
        continue
    urlscrap=x[0]
    print '%s  %s'%(cont,urlscrap)  
    ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)#insertar en la bd Link
    ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type

    webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear 
    webpage1 = webpage1.replace('<p>','').replace('</p>','').replace('<br>','')
    #webpage1 = requests.get(urlscrap)
    soup1 = BeautifulSoup(webpage1)#.text)

    banderaOer=False
    
    htmlCurso = soup1.select('div.colright')#html del curso
    if htmlCurso==[]:
        continue
    

    ObjBd.insertar_datos_trip(urlscrap,'html',str(htmlCurso[0]),tabla)

    hrefs= htmlCurso[0].find_all('a', href=True)
    #print hrefs
    #print htmlCurso
    #break

    """
    if hrefs!=[]:
        #print 'Si hay oer'
        banderaOer=True
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','1',tabla)
    else:
        pass
        #print 'No hay Oers'
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)
    """
    
    for href in hrefs:
        urlOer=unionurl(urlscrap,href.get('href'))
        if 'view.php?' in urlOer:
            diviurl= urlOer.split('view.php?')
            urlOer=diviurl[0]+'view.php?'+'inpopup=true&'+diviurl[1]
        try:
            extoer=identificarOer(urlOer)
        except Exception, e:
            continue
        
        
        if extoer=='0':
            continue
        print href.get('href')

        aux=href.previous_element
        while len(str(aux).replace(' ','').strip())<=3 or str(aux)[0]=='<':
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

        textoOer=href.text
        
        #print '            %s'%descripOer
        #print '            %s'%textoOer
        #print '            %s'%urlOer
        #print '            %s'%str(htmlOer)[0:10]


        ObjBd.insertar_datos_trip(urlscrap,'oer',urlOer,tabla)
        ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
        ObjBd.insertar_datos_trip(urlOer,'title',descripOer ,tabla)
        ObjBd.insertar_datos_trip(urlOer,'description',textoOer,tabla)
        ObjBd.insertar_datos_trip(urlOer,'html',str(htmlOer),tabla)

        #extoer=extraerextoer(urlOer)
        ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
        ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)

