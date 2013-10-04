#-*-coding: utf-8 -*-

import codecs

from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata

ObjBd = BDdatos()
datos=ObjBd.datos_start_url('link_cursos')
count=0
for x in datos:
	menus=ObjBd.menus(x[1])
	if menus==():
		print 'Vacio'
	else:
		print 'Lleno'
	for menu in menus:
		count=count+1

	if count==0:
		print x[1]
		ObjBd.insertar_cursosvacios(x[1],'cursoavacios')
	count=0