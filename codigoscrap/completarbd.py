#-*-coding: utf-8 -*-
import re,string
from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def extraernombremenu(urlmenu):
    url=urlmenu.split('/')
    return url[len(url)-1]

def extraerextoer(urlmenu):
    url=urlmenu.split('.')
    return url[len(url)-1]
tabla='CursosMit'
ObjBd = BDdatos()
datos=ObjBd.prueba()
#print datos
for cont,x in enumerate(datos):
	link=x[0]
	print cont
	print link
	ObjBd.insertar_datos_trip(link,'rdf:type','ocw',tabla)