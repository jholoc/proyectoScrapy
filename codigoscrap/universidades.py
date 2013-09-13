#-*-coding: utf-8 -*-

import codecs

from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata


ObjBd = BDdatos()
datos=ObjBd.datos_start_url_orden('OCWC_cursos')
url4=''
for x in datos:
	url=x[3]
	url2=url.split('/')
	url3= url2[2]
	ObjBd.insertar_datos_CursoUrlSeparado(url3,url,'CursosUrlSeparado')
	if url3 != url4:
		print url3
		url4=url3