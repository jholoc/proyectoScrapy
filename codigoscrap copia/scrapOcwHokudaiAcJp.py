#-*-coding: utf-8-sig -*-
import re,string
from bs4 import *
from urllib import urlopen
from bd import *
#import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def unionurl(urlpag,urloer):
    if 'http://' in urloer:
        return urloer
    else:
        list1= urlpag.split('/')
        list2= urloer.split('/')
        list1.extend([element for element in list2 if element not in list1])
        union= '/'.join(list1)
        return str(union)
def extraerextoer(urlmenu):
    url=urlmenu.split('.')
    return url[len(url)-1]

tabla='CursosHokudaiAcJp'


ObjBd = BDdatos()
datos=ObjBd.CursosOcwHokudaiAcJp()
urlscrap='http://oer.avu.org/handle/123456789/139'


for cont,x in enumerate(datos):
	if cont<0:
		continue
	urlscrap=x[0]
	print '%s  %s'%(cont,urlscrap) 
	webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear
	soup1 = BeautifulSoup(webpage1)	
	htmlOcw=webpage1

	soup1 = soup1.select('#MAIN') 
	if soup1==[]:
		continue


	ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)#insertar en la bd Link
	ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type
	ObjBd.insertar_datos_trip(urlscrap,'html',str(htmlOcw),tabla)#insertar en la bd html



	TablaSoup = soup1[0].select("table.dd > tr")
	for tablaoer in TablaSoup:
		columnas=tablaoer.select('td')

		if columnas != [] and columnas[1].text.strip()!="":
			#urlOer=unionurl('http://oer.avu.org',columnas[0].a.get('href'))
			if columnas[0].select('a')==[]:
				continue
			urlOer=unionurl(urlscrap[0:len(urlscrap)-1],columnas[0].a.get('href'))
			print urlOer
			titulOer=columnas[1].text.strip()
			print titulOer
			descripcionOer=columnas[1].text.strip()
			print descripcionOer
			extoer=extraerextoer(urlOer)
			print extoer

			ObjBd.insertar_datos_trip(urlscrap,'oer',urlOer,tabla)
			ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
			ObjBd.insertar_datos_trip(urlOer,'title',titulOer ,tabla)
			ObjBd.insertar_datos_trip(urlOer,'description',descripcionOer,tabla)

			ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
			ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)