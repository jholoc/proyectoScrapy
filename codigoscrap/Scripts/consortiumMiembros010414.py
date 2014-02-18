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
def buscauniversidad(basedeuniversidades,nombredeuniversidad):
    for universidad in basedeuniversidades:
        if universidad[2]==nombredeuniversidad:
            return universidad[0]
            break
    return 'null'





host=sys.argv[1]
bd=sys.argv[2]
tabla=sys.argv[3]
user=sys.argv[4]
clave=sys.argv[5]


ObjBd = BDdatos()
ObjBd.configuracionLord(host,user,clave,bd)
ObjBd.crearTablalord(tabla)
#sys.exit()

urlscrap='http://www.ocwconsortium.org/members/'
print urlscrap
paises= bs4extracion(urlscrap,"ul.country-list > li > a")
InicioPag='http://www.ocwconsortium.org'


for cont,i in enumerate(paises):
    if cont==0:
        continue

    titulo_paises=i.text
    url_paises=InicioPag+i.get('href')
    print titulo_paises
    print '    %s'%url_paises

    universidadesExtraidos=bs4extracion(url_paises,'.large-9 > table > tr')
    for filas in universidadesExtraidos:
        columnas=filas.select('td')   
        universidadtitulo=columnas[0].a.text
        linkuniversidad=InicioPag+columnas[0].a.get('href')
        tipodeuniversidad=columnas[1].text
        if columnas[2].text=='':
            miembrode='null'
        else:
            miembrode=columnas[2].text
        print '        %s'%universidadtitulo
        print '        %s'%linkuniversidad
        linkuniversidad2=buscauniversidad(ConsortiumMienmbro,universidadtitulo)
        print '        \033[1m%s\033[0m'%linkuniversidad2
        print '        %s'%tipodeuniversidad
        print '        %s'%miembrode
        ObjBd.insertar_datos_trip_lord(linkuniversidad,'rdf:type','locwd:ocwMember',tabla)

        ObjBd.insertar_datos_trip_lord(linkuniversidad,'rdf:type','ocwRepositorio',tabla)
        ObjBd.insertar_datos_trip_lord(linkuniversidad,'urlOCWC',linkuniversidad,tabla)
        ObjBd.insertar_datos_trip_lord(linkuniversidad,'urlOCWC2',linkuniversidad2,tabla)

        ObjBd.insertar_datos_trip_lord(linkuniversidad,'countryOcwc',titulo_paises,tabla)
        ObjBd.insertar_datos_trip_lord(linkuniversidad,'titleInstitutionalRepoOcwc',universidadtitulo,tabla)
        ObjBd.insertar_datos_trip_lord(linkuniversidad,'typeMemberOcwc',tipodeuniversidad,tabla)
        ObjBd.insertar_datos_trip_lord(linkuniversidad,'MemberOcwc',miembrode,tabla)


        universidad=bs4extracion(linkuniversidad,'div.large-9')[0]
        descripcionuniversidad=universidad.select('p.large-8')[0].text
        print'            %s'%descripcionuniversidad[0:100]

        ObjBd.insertar_datos_trip_lord(linkuniversidad,'descriptionRepoOcwc',descripcionuniversidad,tabla)

        hrefs= universidad.find_all('a', href=True)
        for link in hrefs:
            #print'            %s   %s'%(link.previous_element.previous_element,link.get('href'))
            if link.previous_element.previous_element=='Main Website:':
                print'            urlmainWebsite   %s'%(link.get('href'))
                purl=link.get('href')
                ObjBd.insertar_datos_trip_lord(linkuniversidad,'urlInstitutionalRepo',link.get('href'),tabla)
            
            elif link.previous_element.previous_element=='OCW Website:':
                print'            urlocwWebsite   %s'%(link.get('href'))
                purl=link.get('href')

                ObjBd.insertar_datos_trip_lord(linkuniversidad,'urlOcwRepo',link.get('href'),tabla)

        ObjBd.insertar_datos_trip_lord(linkuniversidad,'purl',purl,tabla)

        if universidad.select('img')!=[]:
            logouniversidad=universidad.select('img')[0].get('src')
            print '            IMAGEN= %s'%logouniversidad
        else:
            logouniversidad='null'
            print '            IMAGEN= NULL'

        ObjBd.insertar_datos_trip_lord(linkuniversidad,'urlImageRepoOcwc',logouniversidad,tabla)


