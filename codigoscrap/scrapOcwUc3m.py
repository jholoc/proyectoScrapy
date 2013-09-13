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

#texto='      nose ojala esets kdslknmfs   dsfoks      '
#print texto.strip(' ')
#print texto.replace(' ','')

tabla='CursosUc3m'

ObjBd = BDdatos()
datos=ObjBd.cursosuc3()
urlscrap='http://ocw.uc3m.es/ingenieria-telematica/telematica'

for cont,x in enumerate(datos):


    urlscrap=x[0]
    print '%s  %s'%(cont,urlscrap)
    ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)
    webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear
    soup1 = BeautifulSoup(webpage1)
    tiSoup = soup1.select(".portletItem")#selecion de la pagina que contiene los titulos de las noticias
    
    banderaOer=False

    for i in tiSoup:
        tituloMenu=i.a.text.strip()
        urlMenu=unionurl(urlscrap,i.a.get('href'))

        if urlMenu==urlscrap:
            continue

        patron=re.compile('\.(pdf/view|mp3/view|tar/view|gz/view|html/view|mdb/view|mp3|zip|tar|gz|html|mdb|txt|txt/view)$')
        M=re.findall(patron,urlMenu)
        if M!=[]:
            continue
        
        #print tituloMenu
        #print urlMenu

        ObjBd.insertar_datos_trip(urlscrap,'menu',urlMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'link',urlMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'title',tituloMenu,tabla)
        

        webpage2=urlopen(urlMenu).read()
        soup2=BeautifulSoup(webpage2)
        soup2=soup2.find(id='content')
        htmlCurso=soup2

        ObjBd.insertar_datos_trip(urlMenu,'html',str(htmlCurso),tabla)

        if soup2==None:
            #print 'No hay Oers'
            ObjBd.insertar_datos_trip(urlMenu,'existenOer','0',tabla)
            continue
        hrefs= soup2.find_all(href=re.compile("(http://ocw.uc3m.es)\w\.(pdf/view|mp3/view|zip/view|zip/at_download/file|tar/view|gz/view|html/view|mdb/view|mp3|zip|tar|gz|html|mdb|txt|txt/view)|/view|/at_download/file$"))

        if hrefs!=[]:
            #print 'Si hay oer'
            banderaOer=True
            ObjBd.insertar_datos_trip(urlMenu,'existenOer','1',tabla)
        else:
            #print 'No hay Oers'
            ObjBd.insertar_datos_trip(urlMenu,'existenOer','0',tabla)

        for href in hrefs:
            aux=href.previous_element
            while len(str(aux).replace(' ',''))<=3 or str(aux)[0]=='<':
                if str(aux)[0]=='<':
                    if str(aux)[1]=='a':
                        break
                        #aux=''
                    else:
                        if str(aux)[1]=='t' or str(aux)[1]=='i'or str(aux)[1]=='s'or str(aux)[1]=='e':
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
                    descripOer=removersignos(aux.text).strip() #aux.text
                    #print '    %s'% descripOer
            else:
                htmlOer=aux.parent
                descripOer=removersignos(aux).strip() #aux
                #print '   %s'%descripOer

            textoOer=href.text.strip()
            urlOer=unionurl(urlscrap,href.get('href').strip('/at_download/file').strip('/view'))#unionurl(urlscrap,href.get('href'))
            #print htmlOer
            #print '            %s'%textoOer
            #print '            %s'%urlOer #href.get('href').strip('/at_download/file').strip('/view')


            ObjBd.insertar_datos_trip(urlMenu,'oer',urlOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'titlte',descripOer ,tabla)
            ObjBd.insertar_datos_trip(urlOer,'description',textoOer,tabla)
            ObjBd.insertar_datos_trip(urlMenu,'html',str(htmlOer),tabla)

    if banderaOer==True:
        #print 'SI HAY OERS'
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','1',tabla)
    else:
        print 'NO HAY OERS'
        print urlscrap
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)
