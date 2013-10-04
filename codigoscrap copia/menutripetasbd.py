#-*-coding: utf-8 -*-

import codecs

from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata




def unionurl(urlpag,urloer):
	if 'http://' in urloer:
		return urloer
	else:
		list1= urlpag.split('/')
		#print list1
		list2= urloer.split('/')
		#print list2

		list1.extend([element for element in list2 if element not in list1])
		#print list1

		union= '/'.join(list1)
		return union

ObjBd = BDdatos()
datos=ObjBd.datos_start_url('link_cursos')
for x in datos:
	#print x[1]
	print '%s -> %s ->%s'%(x[1],'url',x[1])
	ObjBd.insertar_datos_trip(x[1],'url',x[1],'tripletaCursos')
	menus=ObjBd.menus(x[1])
	for menu in menus:
		#print '    %s'%menu[2]
		print '%s -> %s ->%s'%(x[1],menu[1],menu[2])
		print '%s -> %s ->%s'%(menu[2],'url',menu[2])

		ObjBd.insertar_datos_trip(x[1],menu[1],menu[2],'tripletaCursos')
		ObjBd.insertar_datos_trip(menu[2],'url',menu[2],'tripletaCursos')

		recursomenus=ObjBd.recursomenus(menu[2])

		for enurecursomenu,recursomenu in enumerate(recursomenus):
			#print '        \033[1m%s\033[0m : %s'%(recursomenu[1],recursomenu[2])
			if enurecursomenu%2 != 0:
				print '%s -> %s ->%s'%(menu[2],recursomenus[0][1],recursomenus[0][2])
				ObjBd.insertar_datos_trip(menu[2],recursomenus[0][1],recursomenus[0][2],'tripletaCursos')
				oersmenus=ObjBd.oersmenus(recursomenu[2])
				for oermenus in oersmenus:
					if oermenus[2]!='Sin Objeto':

						#print'            --%s'%unionurl(recursomenu[2],oermenus[2])
						print '%s -> %s ->%s'%(menu[2],oermenus[1],unionurl(recursomenu[2],oermenus[2]))
						print '%s -> %s ->%s'%(unionurl(recursomenu[2],oermenus[2]),'url',unionurl(recursomenu[2],oermenus[2]))

						ObjBd.insertar_datos_trip(menu[2],oermenus[1],unionurl(recursomenu[2],oermenus[2]),'tripletaCursos')
						ObjBd.insertar_datos_trip(unionurl(recursomenu[2],oermenus[2]),'url',unionurl(recursomenu[2],oermenus[2]),'tripletaCursos')

						infoers=ObjBd.infoers(unionurl(recursomenu[2],oermenus[2]))
						for infoer in infoers:
							#print'                %s'%infoer[3]
							print '%s -> %s ->%s'%(unionurl(recursomenu[2],oermenus[2]),infoer[2],infoer[3])

							ObjBd.insertar_datos_trip(unionurl(recursomenu[2],oermenus[2]),infoer[2],infoer[3],'tripletaCursos')

	
						
