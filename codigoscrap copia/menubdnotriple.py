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
	menus=ObjBd.menus(x[1])
	if menus==():
		print x[1]
		ObjBd.insertar_datos(x[1],'','','','','cursostabla')
	for menu in menus:
		#print '    %s'%menu[2]

		recursomenus=ObjBd.recursomenus(menu[2])

		for enurecursomenu,recursomenu in enumerate(recursomenus):
			#print '        \033[1m%s\033[0m : %s'%(recursomenu[1],recursomenu[2])
			if enurecursomenu%2 != 0:

				oersmenus=ObjBd.oersmenus(recursomenu[2])
				if oersmenus==():
					print '%s###%s###%s'%(x[1],menu[2],recursomenus[0][2])
					ObjBd.insertar_datos(x[1],menu[2],recursomenus[0][2],'','','cursostabla')
				for oermenus in oersmenus:
					if oermenus[2]!='Sin Objeto':
						print '%s###%s###%s###%s'%(x[1],menu[2],recursomenus[0][2],unionurl(recursomenu[2],oermenus[2]))
						ObjBd.insertar_datos(x[1],menu[2],recursomenus[0][2],unionurl(recursomenu[2],oermenus[2]),'','cursostabla')
						oermenustitulo=ObjBd.oersmenustitulo(oermenus[2])
						if oermenustitulo!=():
							print '%s###%s###%s###%s####%s'%(x[1],menu[2],recursomenus[0][2],unionurl(recursomenu[2],oermenus[2]),oermenustitulo[0][2])
							ObjBd.insertar_datos(x[1],menu[2],recursomenus[0][2],unionurl(recursomenu[2],oermenus[2]),oermenustitulo[0][2],'cursostabla')