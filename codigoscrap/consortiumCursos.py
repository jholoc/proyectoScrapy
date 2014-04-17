#-*-coding: utf-8 -*-
import re,string
from bs4 import *
from urllib import urlopen
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bd import *

def bs4extracion(urlparaestraer,extraesto):
    webpage = urlopen(urlparaestraer).read()
    soup = BeautifulSoup(webpage)
    extracion = soup.select(extraesto)
    return extracion
def validapaguinacion(paginacion):
    bandera='no'
    for pag in paginacion:
        if pag.get('class')[0] == 'next-page':
            bandera=pag.get('href')
    return bandera



#tabla=sys.argv[1]
tabla='ConsortiumCursos310314'
#tabla='ConsortiumTodo'
ObjBd = BDdatos()
ObjBd.crearTabla(tabla)
#sys.exit()



urlscrap='http://www.ocwconsortium.org/providers/'
print urlscrap

webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear  
soup1 = BeautifulSoup(webpage1)
universidades = soup1.select(".large-9 > ul > li")#selecion de la pagina que contiene los titulos de las noticias
InicioPag='http://www.ocwconsortium.org'


for cont,i in enumerate(universidades):
    if cont<0:
        continue
    print cont
    titulo_universidades=i.text
    url_universidades=InicioPag+i.a.get('href')
    print titulo_universidades
    print '    %s'%url_universidades
    ObjBd.insertar_datos_trip(url_universidades,'rdf:type','locwd:ocwMember',tabla)
    """
    ObjBd.insertar_datos_trip(url_universidades,'titulo',titulo_universidades,tabla)
    ObjBd.insertar_datos_trip(url_universidades,'url',url_universidades,tabla)"""

    ObjBd.insertar_datos_trip(url_universidades,'titleInstitutionalRepoOcwc',titulo_universidades,tabla)
    ObjBd.insertar_datos_trip(url_universidades,'urlOCWC',url_universidades,tabla)



    url_universidad=url_universidades
    while True:


        cursosExtraidos=bs4extracion(url_universidad,'.large-9 > table > tr')
        for filas in cursosExtraidos:
            columnas=filas.select('td')   
            cursotitulo=columnas[0].a.text
            linkcurso=columnas[0].a.get('href')
            lenguaje=columnas[1].text
            linkdetalle=InicioPag+columnas[2].a.get('href')
            
            print'            Curso= %s -> %s'%(cursotitulo,linkcurso)
            print'            Detalles=  %s'%(linkdetalle)
            print'            Lenguaje= %s'%lenguaje

            
            """ObjBd.insertar_datos_trip(url_universidades,'ocw',linkcurso,tabla)
            ObjBd.insertar_datos_trip(linkcurso,'rdf:type','opencourseware',tabla)
            ObjBd.insertar_datos_trip(linkcurso,'url',linkcurso,tabla)
            ObjBd.insertar_datos_trip(linkcurso,'titulo',cursotitulo,tabla)
            ObjBd.insertar_datos_trip(linkcurso,'lenguaje',lenguaje,tabla)
            ObjBd.insertar_datos_trip(linkcurso,'urldetalle',linkdetalle,tabla)"""

            ObjBd.insertar_datos_trip(linkcurso,'urlProfileRepoOcwc',url_universidades,tabla)
            ObjBd.insertar_datos_trip(linkcurso,'rdf:type','courseOCWC',tabla)  
            ObjBd.insertar_datos_trip(linkcurso,'urlCourseOCWC',linkcurso,tabla)
            ObjBd.insertar_datos_trip(linkcurso,'titleOer',cursotitulo,tabla)
            ObjBd.insertar_datos_trip(linkcurso,'titleOcwc',cursotitulo,tabla)
            ObjBd.insertar_datos_trip(linkcurso,'languageOcwc',lenguaje,tabla)
            print cont
            try:
                detallecurso=bs4extracion(linkdetalle,'.large-9')
                descripcioncurso= detallecurso[0].select('p')[0].text
                autorcursos= detallecurso[0].select('p > strong')
            except Exception, e:
                print e
                continue
            for autor in autorcursos:
                if autor.text=='Author:':
                    autorcurso=autor.next_element.next_element
            if autorcurso==' ':
                print '            Author= null'
                autorcurso='null'
            else:
                print '            Author= %s'%autorcurso
            try:
                ObjBd.insertar_datos_trip(linkcurso,'descriptionOerOcwc',descripcioncurso,tabla)
                ObjBd.insertar_datos_trip(linkcurso,'descriptionOcwc',descripcioncurso,tabla)
                ObjBd.insertar_datos_trip(linkcurso,'authorOcwc',autorcurso,tabla)
            except Exception, e:
                print e
                continue
            
            

        paginacion=bs4extracion(url_universidad,'.pagination > a')
        validapag=validapaguinacion(paginacion)
        if validapag == 'no':
            break
        url_universidad=url_universidades+validapag

    
