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
	patron = re.compile("(\.(pdf|mp3|mp4|wmv|zip|tar|gz|htm|xls|xlsx|doc|docx|odt|ppt|pptx|XLS|DOCX|PPTX|jpg)$)") 
	patronYoutube=re.compile("www.youtube.com/watch") 
	busquedayt=patronYoutube.search(url)
	if busquedayt!=None:
		return'video Youtube'
	busqueda=patron.search(url)
	try:
		if busqueda==None:			
			urlOpen=urllib.urlopen(url)
			infoUrl=urlOpen.info()['Content-Type']
			if infoUrl=='application/pdf':
				return 'pdf'
			else:
				if infoUrl=='application/zip':
					return 'zip'
				else:
					return '0'
		else:
			return extraerextoer(url)
	except Exception, e:
				return '0'

tabla='CursosNottinghamAcUk'


ObjBd = BDdatos()
datos=ObjBd.CursosOcwNottinghamAcUk()
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
    webpage1 = requests.get(urlscrap)
    soup1 = BeautifulSoup(webpage1.text)

    banderaOer=False
    
    htmlCurso = soup1#.select('#main')#html del curso
    

    ObjBd.insertar_datos_trip(urlscrap,'html',str(htmlCurso),tabla)

    hrefs= htmlCurso.find_all('a', href=True)
    #print hrefs
    #print htmlCurso
    #break

    if hrefs!=[]:
        #print 'Si hay oer'
        banderaOer=True
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','1',tabla)
    else:
        pass
        #print 'No hay Oers'
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)
    for href in hrefs:
    	urlOer=unionurl('http://unow.nottingham.ac.uk/resources',href.get('href'))
    	extoer=identificarOer(href.get('href'))
        #print extoer
        if extoer=='0':
            continue
        print href.get('href')

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


    if banderaOer==True:
        pass
        #print 'SI HAY OERS'
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','1',tabla)
    else:
        print 'NO HAY OERS'
        print urlscrap
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)