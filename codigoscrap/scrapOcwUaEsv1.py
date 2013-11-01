#-*-coding: utf-8-sig -*-
import re,string
from bs4 import *
from urllib import urlopen
from bd import *
#import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
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
        return str(union)
def extraerextoer(urlmenu):
    url=urlmenu.split('.')
    return url[len(url)-1]

tabla='CursosUaEs'


ObjBd = BDdatos()
datos=ObjBd.CursosOcwUaEs()
urlscrap='http://oer.avu.org/handle/123456789/139'


for cont,x in enumerate(datos):
	if cont<74:
		continue
	urlscrap1=x[0]
	urlMenu=urlscrap1
	print '%s  %s'%(cont,urlscrap1) 
	webpage1 = urlopen(urlscrap1).read() #lectura de la pagina a scrapear
	soup1 = BeautifulSoup(webpage1)
	urlscrap2 = soup1.select("script")
	if urlscrap2== []:
		continue
	urlscrap2 = urlscrap2[0].text.split('"')[1]#abrir la redireccion 

	print '%s  %s'%(cont,urlscrap2) 
	webpage1 = urlopen(urlscrap2).read() #lectura de la pagina a scrapear
	webpage1 = webpage1.replace('<p>','').replace('</p>','').replace('<td>','').replace('</td>','').replace('<br>','')
	soup1 = BeautifulSoup(webpage1)
	htmlOcw=webpage1
	banderaOer=False

	ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap2,tabla)#insertar en la bd Link
	ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type
	ObjBd.insertar_datos_trip(urlscrap,'html',str(htmlOcw),tabla)#insertar en la bd html
	soup1 = soup1.select('#cuerpo') 
	
	if soup1 ==[]:
		continue 
	hrefs= soup1[0].find_all(href=re.compile("(\.(pdf|mp3|mp4|zip|tar|gz|htm|xls|xlsx|doc|docx|odt|ppt|pptx|XLS|DOCX|PPTX)$)|(10045)"))
	if hrefs!=[]:		banderaOer=True
		ObjBd.insertar_datos_trip(urlMenu,'existenOer','1',tabla)
	else:
		ObjBd.insertar_datos_trip(urlMenu,'existenOer','0',tabla)
	for href in hrefs:
		aux=href.previous_element
		while len(str(aux).replace(' ',''))<=12 or str(aux)[0]=='<':
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
				descripOer=removersignos(aux.text).strip()

		else:
			htmlOer=aux.parent
			descripOer=removersignos(aux).strip()

		textoOer=href.text
		urlOer=unionurl(urlscrap,href.get('href'))
		print '            %s'%descripOer
		print '            %s'%textoOer
		print '            %s'%urlOer
		print '            %s'%str(htmlOer)[0:10]


		ObjBd.insertar_datos_trip(urlMenu,'oer',urlOer,tabla)
		ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
		ObjBd.insertar_datos_trip(urlOer,'title',descripOer ,tabla)
		ObjBd.insertar_datos_trip(urlOer,'description',textoOer,tabla)
		ObjBd.insertar_datos_trip(urlOer,'html',str(htmlOer),tabla)

		extoer=extraerextoer(urlOer)
		ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
		ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)