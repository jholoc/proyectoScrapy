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

def BuscaDescrip(aux):
    descripOer=aux
    htmlOer=aux.parent
    while len(str(aux).replace(' ',''))<=3 or str(aux)[0]=='<':
        if str(aux)[0]=='<':
            if str(aux)[1]=='a':
                break
            else:
                if str(aux)[1]=='t' or str(aux)[1]=='i':
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
            descripOer=removersignos(aux.text)
    else:
        htmlOer=aux.parent
        descripOer=removersignos(aux).strip()

    return [descripOer,htmlOer]

tabla='scrapOcwUsEs'

ObjBd = BDdatos()
datos=ObjBd.cursosocwus()
urlscrap='http://openlearn.open.ac.uk/course/view.php?name=M208_2'

for cont,x in enumerate(datos):

    if cont<253 :#esta todo
        continue
    urlscrap=x[0]
    print '%s %s'%(cont,urlscrap)

    ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)#insertar en la bd Link
    ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type

    webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear
    soup1 = BeautifulSoup(webpage1)
    tiSoup = soup1.select("div.unSelected")#selecion de la pagina que contiene los titulos de las noticias

    banderaOer=False

    for i in tiSoup:

        tituloMenu=i.a.text.strip()
        urlMenu=unionurl(urlscrap,i.a.get('href'))

        if urlMenu==urlscrap:
            continue




        ObjBd.insertar_datos_trip(urlscrap,'menu',urlMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'link',urlMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'title',tituloMenu,tabla)
        ObjBd.insertar_datos_trip(urlMenu,'rdf:type','menu',tabla)
        nombreMenu=extraernombremenu(urlMenu)
        ObjBd.insertar_datos_trip(urlMenu,'rdf:type',nombreMenu,tabla)


        webpage2=urlopen(urlMenu).read()
        soup2=BeautifulSoup(webpage2)
        soup2=soup2.find(id='region-content')
        htmlCurso=soup2

        ObjBd.insertar_datos_trip(urlMenu,'html',str(htmlCurso),tabla)

        if soup2==None:
            ObjBd.insertar_datos_trip(urlMenu,'existenOer','0',tabla)
            continue

        hrefs= soup2.find_all(href=re.compile("\.(pdf|mp3|zip|tar|gz|html|htm|xml|doc|docx|jsp)$"))

        if hrefs!=[]:
            banderaOer=True
            ObjBd.insertar_datos_trip(urlMenu,'existenOer','1',tabla)
        else:
            ObjBd.insertar_datos_trip(urlMenu,'existenOer','0',tabla)
        

        for href in hrefs:
            aux=href.previous_element

            descripOer= BuscaDescrip(aux)

            textoOer=href.text
            urlOer=unionurl(urlscrap,href.get('href'))


            ObjBd.insertar_datos_trip(urlMenu,'oer',urlOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'title',descripOer[0] ,tabla)
            ObjBd.insertar_datos_trip(urlOer,'description',textoOer,tabla)
            ObjBd.insertar_datos_trip(urlOer,'html',str(descripOer[1]),tabla)

            extoer=extraerextoer(urlOer)
            ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
            ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)
            
    if banderaOer==True:
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','1',tabla)
    else:
        print 'NO HAY OERS'
        print urlscrap
        ObjBd.insertar_datos_trip(urlscrap,'existenOer','0',tabla)
