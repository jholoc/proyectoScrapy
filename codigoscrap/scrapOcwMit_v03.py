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
    signos=(',','.',';','+','{','}','[',']','(',')','^','~','#','σ')
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

texto='      nose ojala esets kdslknmfs   dsfoks      '
#print texto.strip(' ')
#print texto.replace(' ','')

#839

tabla='CursosMit3'


ObjBd = BDdatos()
datos=ObjBd.cursosmit()
urlscrap='http://ocw.mit.edu/courses/mechanical-engineering/2-29-numerical-fluid-mechanics-fall-2011'
for cont,x in enumerate(datos):
    if cont<0:
        continue
    urlscrap=x[0]
    print '%s  %s'%(cont,urlscrap)  
    #ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)#insertar en la bd Link
    #ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type

    webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear 
    webpage1 = webpage1.replace('<p>','').replace('</p>','').replace('<br>','')
    soup1 = BeautifulSoup(webpage1)
    tiSoup = soup1.select("li.")#selecion de la pagina que contiene los titulos de las noticias

    banderaOer=False

    for i in tiSoup:
        tituloMenu=i.a.text.strip()
        urlMenu=unionurl(urlscrap,i.a.get('href'))
        
        ObjBd.insertar_datos_trip(urlscrap,'menu',urlMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'link',urlMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'title',tituloMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'rdf:type','menu',tabla)
        nombreMenu=extraernombremenu(urlMenu)
        ObjBd.insertar_datos_trip(urlMenu,'rdf:type',nombreMenu,tabla)
        try:
            ObjBd.insertar_datos(urlscrap,urlMenu,tituloMenu,'','','cursostabla')
        except Exception, e:
            print e
            continue
        
        
        #print tituloMenu
        #print urlMenu
        
        webpage2=urlopen(urlMenu).read()
        webpage2 = webpage2.replace('<p>','').replace('</p>','')
        soup2=BeautifulSoup(webpage2)
        htmlCurso = soup2.select('#course_inner_section')#html del curso

        ObjBd.insertar_datos_trip(urlMenu,'html',str(htmlCurso),tabla)

        hrefs= soup2.find_all(href=re.compile("\.(pdf|mp3|mp4|zip|tar|gz|html|xls|xlsx|doc|docx|odt|ppt|pptx|gif)$"))

        if hrefs!=[]:
            #print 'Si hay oer'
            banderaOer=True
            #ObjBd.insertar_datos_trip(urlMenu,'existenOer','1',tabla)
        else:
            pass
            #print 'No hay Oers'
            #ObjBd.insertar_datos_trip(urlMenu,'existenOer','0',tabla)
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
                    descripOer=removersignos(aux.text).strip()#aux.text
                    #print '    %s'%descripOer

            else:
                htmlOer=aux.parent
                descripOer=removersignos(aux).strip()#aux
                #print '   %s'%descripOer

            textoOer=href.text
            urlOer=unionurl(urlscrap,href.get('href'))
            #print '            %s'%descripOer
            #print '            %s'%textoOer
            #print '            %s'%urlOer
            #print '            %s'%str(htmlOer)[0:10]

            try:
            ObjBd.insertar_datos_trip(urlMenu,'oer',urlOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'title',descripOer ,tabla)
            ObjBd.insertar_datos_trip(urlOer,'description',textoOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'html',str(htmlOer),tabla)

            extoer=extraerextoer(urlOer)
            ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
            ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)
              
            except Exception, e:
                print e
                continue

            



    if banderaOer==True:
        pass
        #print 'SI HAY OERS'
        #ObjBd.insertar_datos_trip(urlscrap,'existenOer','1',tabla)
    else:
        print 'NO HAY OERS'
        print urlscrap
        #ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)