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

    return [descripOer,htmlOer]



tabla='CursosUnivalleEduCo'

ObjBd = BDdatos()
#ObjBd.crearTabla(tabla)
#sys.exit()

datos=ObjBd.CursosOcwUnivalleEduCo()


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
    tiSoup = soup1.select("#portlet-eduCommonsNavigation > div.unSelected")#selecion de la pagina que contiene los titulos de las noticias

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
        
        #print tituloMenu
        print urlMenu
        
        webpage2=urlopen(urlMenu).read()
        webpage2 = webpage2.replace('<p>','').replace('</p>','')
        soup2=BeautifulSoup(webpage2)
        htmlCurso = soup2.select('.plain')#html del curso

        if htmlCurso==[]:
            htmlCurso = soup2.select('#region-content')#html del curso
        if htmlCurso==[]:
            continue

        ObjBd.insertar_datos_trip(urlMenu,'html',str(htmlCurso),tabla)
        hrefs= htmlCurso[0].find_all('a', href=True)
        if hrefs!=[]:
            #print 'Si hay oer'
            banderaOer=True
            ObjBd.insertar_datos_trip(urlMenu,'existenOer','1',tabla)
        else:
            pass
            #print 'No hay Oers'
            ObjBd.insertar_datos_trip(urlMenu,'existenOer','0',tabla)

        for href in hrefs:
            try:
                urlOer=unionurl(urlscrap,href.get('href')) 
                if urlOer.count('http://')>1:
                    continue
                patron = re.compile("/view$")
                busqueda=patron.search(urlOer)
                textoOer=''
                if busqueda!=None:
                    webpage3=urlopen(urlOer).read()
                    soup3=BeautifulSoup(webpage3)
                    htmlOerView = soup3.select('#region-content')
                    textoOer=htmlOerView[0].select('h1')[0].text
                    #urlOer=htmlOerView[0].select ('.objectMetadata')
                    urlOer=htmlOerView[0].select('p')[0].a.get('href') #find_all('a', href=True)[4].get('href')
                    urlOer=unionurl(urlscrap,urlOer)


                extoer=identificarOer(urlOer)
            except Exception, e:
                continue
            
            if extoer=='0':
                continue
            
            print urlOer
            decripOer=EncuentraDescripcion(href.previous_element)
            if textoOer!='':
                textoOer=href.text
            descripOer=decripOer[0]
            htmlOer=decripOer[1]
            
            ObjBd.insertar_datos_trip(urlMenu,'oer',urlOer,tabla)
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