#-*-coding: utf-8 -*-
import re,string
from bs4 import *
from urllib import urlopen
from bd import *
from scrapUniversidades import *
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

ObjBd = BDdatos()
Scrapear = Scrap()
def cursos(datos,tabla):
    for cont,x in enumerate(datos):
        if cont<1753: 
            continue
        print cont
        Scrapear.ScrapUniverdidades(x[0],tabla)

host=sys.argv[1]
bd=sys.argv[2]
tabla=sys.argv[3]
user=sys.argv[4]
clave=sys.argv[5]


ObjBd = BDdatos()
ObjBd.configuracionLord(host,user,clave,bd)
ObjBd.crearTablalord(tabla)
datos=ObjBd.CursosConsortium()
cursos(datos,tabla)

#sys.exit()