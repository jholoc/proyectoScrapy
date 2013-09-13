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

listaparabd=[]
ObjBd = BDdatos()
datos=ObjBd.datos_start_url('link_cursos')
for x in datos:
	print x[1]

	menus=ObjBd.menus(x[1])
	for menu in menus:
		print '    \033[1m%s\033[0m : %s'%(menu[1],menu[2])

		recursomenus=ObjBd.recursomenus(menu[2])
		for enurecursomenu,recursomenu in enumerate(recursomenus):
			print '        \033[1m%s\033[0m : %s'%(recursomenu[1],recursomenu[2])
			listaparabd.append(x[1])
			if enurecursomenu%2 != 0:
				#print 'AQUIIII %s/'%recursomenu[2]
				#oersmenus=ObjBd.oersmenus('%s/'%recursomenu[2])
				oersmenus=ObjBd.oersmenus(recursomenu[2])

				for oermenus in oersmenus:
					if oermenus[2]!='Sin Objeto':
						#print'            %s'%oermenus[2]
						print'              \033[1m%s\033[0m : %s'%(oermenus[1],unionurl(recursomenu[2],oermenus[2]))

						infoers=ObjBd.infoers(unionurl(recursomenu[2],oermenus[2]))
						for infoer in infoers:
							print'                \033[1m%s\033[0m : %s'%(infoer[2],infoer[3])

					#print '%s-%s-'%x[1] 
