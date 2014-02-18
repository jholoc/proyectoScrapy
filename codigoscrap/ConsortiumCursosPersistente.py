import re,string
from bs4 import *
from urllib import urlopen
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bd import *
def cambiosujeto(sujeto,tabla):
	urlpersis=''
	for fila in tabla:
		if fila[0]==sujeto:
			urlpersis=fila[1]
			break
	return urlpersis


#tabla='ConsortiumCursos'
#tabla='ConsortiumTodo'
tabla='ConsortiumCursosPersistencia'
ObjBd = BDdatos()
#ObjBd.crearTabla(tabla)
#sys.exit()
cursosBusca=ObjBd.datos_start_url('ConsortiumBuscaMiembros')
cursos=ObjBd.datos_start_url('ConsortiumCursos')
for filacurso in cursos:
	s=filacurso[0]
	p=filacurso[1]
	o=filacurso[2]
	if 'www.ocwconsortium.org' in filacurso[0]:
		if filacurso[1]=='urlOCWC':
			#print 's p o %s %s'%(cambiosujeto(filacurso[0],cursosBusca),cambiosujeto(filacurso[2],cursosBusca))
			sp=cambiosujeto(filacurso[0],cursosBusca)
			op=cambiosujeto(filacurso[2],cursosBusca)
			ObjBd.insertar_datos_trip_lord(s,p,o,sp,op,tabla)
			continue
		else:
			#print 's p o %s o'%cambiosujeto(filacurso[0],cursosBusca)
			sp=cambiosujeto(filacurso[0],cursosBusca)
			ObjBd.insertar_datos_trip_lord(s,p,o,sp,o,tabla)
			continue

	elif filacurso[1]=='urlProfileRepoOcwc':
		#print 's p o s %s'%cambiosujeto(filacurso[2],cursosBusca)
		op=cambiosujeto(filacurso[2],cursosBusca)
		ObjBd.insertar_datos_trip_lord(s,p,o,s,op,tabla)
		continue
	#print 's p o s o'
	ObjBd.insertar_datos_trip_lord(s,p,o,s,o,tabla)

