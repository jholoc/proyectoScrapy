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

tabla='CursosAvuOrg'


ObjBd = BDdatos()
datos=ObjBd.CursosOcwAvuOrg()
urlscrap='http://oer.avu.org/handle/123456789/139'


for cont,x in enumerate(datos):
	if cont<0:
		continue
	urlscrap=x[0]
	print '%s  %s'%(cont,urlscrap) 
	webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear
	soup1 = BeautifulSoup(webpage1)
	htmlOcw=webpage1 


	ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)#insertar en la bd Link
	ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type
	ObjBd.insertar_datos_trip(urlscrap,'html',str(htmlOcw),tabla)#insertar en la bd html



	TablaSoup = soup1.select("table.file-list.ds-table > tr")
	for tablaoer in TablaSoup:
		columnas=tablaoer.select('td')
		if columnas != []:
			urlOer=unionurl('http://oer.avu.org',columnas[0].a.get('href'))
			titulOer=columnas[4].text
			descripcionOer=columnas[0].a.text
			extoer=columnas[2].text
			print urlOer

			ObjBd.insertar_datos_trip(urlscrap,'oer',urlOer,tabla)
			ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
			ObjBd.insertar_datos_trip(urlOer,'title',titulOer ,tabla)
			ObjBd.insertar_datos_trip(urlOer,'description',descripcionOer,tabla)

			ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
			ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)