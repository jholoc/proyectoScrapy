#-*-coding: utf-8-sig -*-
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

def ViewContenido(urlscrap,descripOer,extoer,htmlOer):
    webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear
    soup1 = BeautifulSoup(webpage1)
    
    soup1=soup1.find(id='content')
    if soup1!=None:
        UrlsOer = soup1.find_all(href=re.compile("\.(pdf|mp3|zip|tar|gz|html|xls|doc|docx|xlsx|ppt|pptx|odt|csv|swf|fl)$"))
        if UrlsOer!=[]:
            UrlOer=unionurl(urlscrap,UrlsOer[0].get('href'))
            #print '                %s'%UrlOer
            TituloOer= soup1.select('#parent-fieldname-title')[0]
            TituloOer=str(TituloOer.text).strip()  
            AutorOer= soup1.select('p.documentByLine')
            if soup1.select('p.documentByLine')==[]:
                AutorOer='No existe autor'
            else:
                AutorOer= AutorOer[0] 
                AutorOer=str(AutorOer.text).strip()
            
            

            ObjBd.insertar_datos_trip(urlscrap,'link',UrlOer,tabla)
            ObjBd.insertar_datos_trip(urlscrap,'title',TituloOer ,tabla)
            ObjBd.insertar_datos_trip(urlscrap,'description',descripOer,tabla)
            ObjBd.insertar_datos_trip(urlscrap,'html',str(htmlOer),tabla)
            
            ObjBd.insertar_datos_trip(urlscrap,'autor',AutorOer,tabla)

            extoer=extraerextoer(UrlOer)
            
            ObjBd.insertar_datos_trip(urlscrap,'rdf:type','oer',tabla)
            ObjBd.insertar_datos_trip(urlscrap,'rdf:type',extoer,tabla)
        else:
            ObjBd.insertar_datos_trip(urlscrap,'link','OFFLINE',tabla)




tabla='CursosUpmEs'


ObjBd = BDdatos()
datos=ObjBd.CursosOcwUpmEs()
urlscrap='http://ocw.uc3m.es/ingenieria-telematica/telematica'

for cont,x in enumerate(datos):

    if cont!=97: 

        continue
    urlscrap=x[0]
    print '%s  %s'%(cont,urlscrap)
    ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)
    ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)
    webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear
    soup1 = BeautifulSoup(webpage1)
    
    tiSoup = soup1.select("dl#portlet-simple-nav > dd.portletItem")#selecion de la pagina que contiene los titulos de las noticias
    
    banderaOer=False

    for i in tiSoup:
        tituloMenu=i.a.text.strip()
        urlMenu=unionurl(urlscrap,i.a.get('href'))

        if urlMenu==urlscrap:
            continue

        patron=re.compile('.zip$')
        M=re.findall(patron,urlMenu)
        if M!=[]:
            continue

        patron=re.compile('/view$')
        M=re.findall(patron,urlMenu)
        if M!=[]:
            ObjBd.insertar_datos_trip(urlscrap,'oer',urlMenu,tabla)

            ViewContenido(urlMenu,tituloMenu,'zip',i)
            continue


        ObjBd.insertar_datos_trip(urlscrap,'menu',urlMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'link',urlMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'title',tituloMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'rdf:type','menu',tabla)
        nombreMenu=extraernombremenu(urlMenu)
        ObjBd.insertar_datos_trip(urlMenu,'rdf:type',nombreMenu,tabla)


        

        webpage2=urlopen(urlMenu).read()
        webpage2 = webpage2.replace('<p>','').replace('</p>','')
        soup2=BeautifulSoup(webpage2)
        soup2=soup2.find(id='content')

        htmlCurso=soup2

        ObjBd.insertar_datos_trip(urlMenu,'html',htmlCurso,tabla)

        if soup2==None:
            ObjBd.insertar_datos_trip(urlMenu,'existenOer','0',tabla)
            continue
        hrefs= soup2.find_all(href=re.compile("((http://ocw.uc3m.es)\w\.|/view)$"))

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
                        #aux=''
                    else:
                        if str(aux)[1]=='t' or str(aux)[1]=='i'or str(aux)[1]=='s' or str(aux)[1]=='e' or str(aux)[1]=='p':
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

            textoOer=href.text.strip()#es el tipo de oer(pdf,zip,etc)
            urlOer=unionurl(urlscrap,href.get('href'))


            ObjBd.insertar_datos_trip(urlMenu,'oer',urlOer,tabla)
            
            ViewContenido(urlOer,descripOer,textoOer,htmlOer)

    if banderaOer==True:
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','1',tabla)
    else:
        print 'NO HAY OERS'
        print urlscrap
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)
