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

tabla='CursosUaEs'


ObjBd = BDdatos()
datos=ObjBd.CursosOcwUaEs()
urlscrap='http://oer.avu.org/handle/123456789/139'


for cont,x in enumerate(datos):
	if cont<7:
		continue
	urlscrap1=x[0]
	print '%s  %s'%(cont,urlscrap1) 
	webpage1 = urlopen(urlscrap1).read() #lectura de la pagina a scrapear
	soup1 = BeautifulSoup(webpage1)

	urlscrap2 = soup1.select("script")[0].text.split('"')[1]#abrir la redireccion 

	print '%s  %s'%(cont,urlscrap2) 
	webpage1 = urlopen(urlscrap2).read() #lectura de la pagina a scrapear
	soup1 = BeautifulSoup(webpage1)
	htmlOcw=webpage1

	soup1 = soup1.select('#cuerpo') 
	
	if soup1 ==[]:
		continue 
	hrefs= soup1[0].find_all(href=re.compile("(\.(pdf|mp3|mp4|zip|tar|gz|html|htm|xls|xlsx|doc|docx|odt|ppt|pptx|XLS|DOCX|PPTX)$)"))
	print hrefs
	if hrefs==None:
		continue
	tablascrap=hrefs[0].parent
	while str(tablascrap)[0:6]!='<table' :
		tablascrap=tablascrap.parent


	#ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap2,tabla)#insertar en la bd Link
	#ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type
	#ObjBd.insertar_datos_trip(urlscrap,'html',str(htmlOcw),tabla)#insertar en la bd html



	TablaSoup = tablascrap.select("tr")
	for tablaoer in TablaSoup:
		columnas=tablaoer.select('td')
		if columnas != []:
			#urlOer=unionurl('http://oer.avu.org',columnas[0].a.get('href'))
			urlOer=columnas[len(columnas)-1].a.get('href')
			print urlOer
			titulOer=columnas[len(columnas)-4].text
			print titulOer
			descripcionOer=columnas[0].text
			print descripcionOer
			extoer=extraerextoer(urlOer)
			print extoer

			#ObjBd.insertar_datos_trip(urlscrap,'oer',urlOer,tabla)
			#ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
			#ObjBd.insertar_datos_trip(urlOer,'title',titulOer ,tabla)
			#ObjBd.insertar_datos_trip(urlOer,'description',descripcionOer,tabla)

			#ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
			#ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)