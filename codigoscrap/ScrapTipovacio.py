import re,string,requests
import re,string
from bs4 import *
from urllib import urlopen
import urllib
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bd import *

def extraerextoer(urlmenu):
        url=urlmenu.split('.')
        return url[len(url)-1]
def identificarOer(url):
    try:
        if identificarOer2(url)=='0':
            print 'if'
            url=requests.get(url).url
            print url
            return identificarOer2(url)
        else:
            print 'else'
            return identificarOer2(url)
    except Exception, e:
        return '0'

def identificarOer2(url):
    patron = re.compile("(\.(html|tgz|pdf|mp3|mp4|MP4|mov|wmv|flv|zip|rar|tar|gz|htm|xls|xlsx|doc|docx|odt|pps|ppt|pptx|XLS|DOCX|PPTX|jpg|gif|ISO|iso|epv|mobipocket|swf|jar|avi|AVI|txt|mpg|MPG|dwg|tg|exe|EXE)$)")
    if "http://www.youtube.com/watch" in url:
        return'video Youtube'
    busqueda=patron.search(url)
    try:
        if busqueda==None:  
            urlOpen=urllib.urlopen(url)
            infoUrl=urlOpen.info()['Content-Type']
            print infoUrl
            if infoUrl=='application/pdf':
                return 'pdf'
            elif infoUrl=='application/zip':
                return 'zip'
            elif infoUrl=='application/octet-stream':
                return 'archivo binario de MIME'
            elif infoUrl=='application/rar':
                return 'rar'
            elif infoUrl=='application/msword':
                return 'dot'
            elif infoUrl=='image/jpeg':
                return 'jpeg'   
            elif infoUrl=='application/pdf;charset=UTF-8':
                return 'pdf'
            elif infoUrl=='video/x-ms-wmv':
                return 'wmv'
            elif infoUrl=='video/x-ms-asf':
                return 'asf'
            elif infoUrl=='video/quicktime':
                return 'mov'
            else:
                return '0'
        else:
            return extraerextoer(url)
    except Exception, e:
            print e
            return '0'
#tabla='ConsortiumCursos'
#tabla='ConsortiumTodo'
tabla='CursosUmichEdu'
ObjBd = BDdatos()
#ObjBd.crearTabla(tabla)
#sys.exit()
#print identificarOer("http://ocw.uc3m.es/tecnologia-electronica/electronic-components-and-circuits/lecture-notes-1/module-ii/OCW-ECC_S13_Introduction_to_field_effect_transistors_FET.pdf/at_download/file")
cursos=ObjBd.datos_start_url('Prueba')
for filacurso in cursos:
	s=filacurso[0]
	p=filacurso[1]
	o=filacurso[2]
	if p=="oer":
		objetoext=identificarOer(o)
		ObjBd.insertar_datos_trip(s,p,o,tabla)
		ObjBd.insertar_datos_trip(o,"rdf:type","oer",tabla)
		ObjBd.insertar_datos_trip(o,"rdf:type",objetoext,tabla)
		print '%s --- %s--- %s'%(s,o,objetoext)
	else:
		ObjBd.insertar_datos_trip(s,p,o,tabla)
#UNIVERSIA
"""cursos=ObjBd.datos_start_url('CursosMit2')
for filacurso in cursos:
	s=filacurso[0]
	p=filacurso[1]
	o=filacurso[2]
	if o==None and p=="rdf:type":
		objetoext=identificarOer(s)
		ObjBd.insertar_datos_trip(s,p,objetoext,tabla)
		print '%s --- %s'%(s,objetoext)
	else:
		ObjBd.insertar_datos_trip(s,p,o,tabla)"""

