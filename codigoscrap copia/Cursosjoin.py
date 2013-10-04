#-*-coding: utf-8 -*-

import codecs

from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata
bandera=0
ObjBd = BDdatos()
datos=ObjBd.datos_start_url('link_cursos')
datos2=ObjBd.datos_start_url('OCWC_cursos')
listaSi=[]
listaNo=[]
contadorNo=0
contadorSi=0
"""for cursos1 in datos:
	bandera=0
	for cursos2 in datos2:
		if cursos1[1] == cursos2[3] or cursos1[1] == '%s/'%cursos2[3]:
			bandera=1
			break
	if bandera==1:
		contadorSi=contadorSi+1
		#listaSi.append(cursos1[1])
		#print 'SI -> %s'%cursos1[1]
	else:
		contadorNo=contadorNo+1
		#listaNo.append(cursos1[1])
		#print 'NO -> %s'%cursos1[1]
print contadorNo"""

for cursos2 in datos2:
	bandera=0
	for cursos1 in datos:
		if cursos1[1] == cursos2[3] or cursos1[1] == '%s/'%cursos2[3]:
			bandera=1
			break
	if bandera==1:
		contadorSi=contadorSi+1
		#listaSi.append(cursos1[1])
		#print 'SI -> %s'%cursos1[1]
	else:
		contadorNo=contadorNo+1
		#listaNo.append(cursos1[1])
		#print 'NO -> %s'%cursos1[1]
print contadorNo