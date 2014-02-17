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

url='http://ocw.uci.edu/lectures/2010_gulf_oil_spill_investigating_its_root_causes_at_the_request_of_the_president.html'
tabla='CursosConsortium'
tabla='prueba'
datos=ObjBd.CursosConsortium()
#datos=ObjBd.CursosConsortiumFaltantes()
cursos(datos,tabla)
#ObjBd.crearTabla(tabla)
#sys.exit()


"""tabla='CursosVideoLectures'
datos=ObjBd.CursosOcwVideoLectures()
cursos(datos,tabla)
#ObjBd.crearTabla(tabla)
sys.exit()

tabla='CursosUvEs'
datos=ObjBd.CursosOcwUvEs()
cursos(datos,tabla)

tabla='CursosAghEduPl'
datos=ObjBd.CursosOcwAghEduPl()
cursos(datos,tabla)

tabla='CursosAvuOrg'
datos=ObjBd.CursosOcwAvuOrg()
cursos(datos,tabla)

tabla='CursosHokudaiAcJp'
datos=ObjBd.CursosOcwHokudaiAcJp()
cursos(datos,tabla)

tabla='CursosIcesiEduCo'
datos=ObjBd.CursosOcwIcesiEduCo()
cursos(datos,tabla)

tabla='CursosInnovaUnedEs'
datos=ObjBd.CursosOcwInnovaUnedEs()
cursos(datos,tabla)


tabla='CursosJhsphEdu'
datos=ObjBd.CursosOcwJhsphEdu()
cursos(datos,tabla)

tabla='CursosKyushuuAcJp'
datos=ObjBd.CursosOcwKyushuuAcJp()
cursos(datos,tabla)

tabla='CursosKoreaEdu'
datos=ObjBd.CursosOcwKoreaEdu()
cursos(datos,tabla)

tabla='CursosLabspaceOpenAcUk'
datos=ExtraeCursos()
cursos(datos,tabla)

tabla='CursosMetropoliaFi'
datos=ObjBd.CursosOcwMetropoliaFi()
cursos(datos,tabla)

tabla='CursosMetuEduTr'
datos=ObjBd.CursosOcwMetuEduTr()
cursos(datos,tabla)

tabla='CursosMit3'
datos=ObjBd.cursosmit()
cursos(datos,tabla)

tabla='CursosNckuEduTw'
datos=ObjBd.CursosOcwNckuEduTw()
cursos(datos,tabla)

tabla='CursosNdEdu'
datos=ObjBd.cursosOcwNdEdu()
cursos(datos,tabla)

tabla='CursosNjitEdu'
datos=ObjBd.CursosOcwNjitEdu()
cursos(datos,tabla)

tabla='CursosNottinghamAcUk'
datos=ObjBd.CursosOcwNottinghamAcUk()
cursos(datos,tabla)

tabla='CursosOpenmarhiRu'
datos=ObjBd.CursosOcwOpenmarhiRu()
cursos(datos,tabla)

tabla='CursosSbuAcIr'
datos=ObjBd.CursosOcwSbuAcIr()
cursos(datos,tabla)

tabla='CursosTmuEduTw'
datos=ObjBd.cursosTmuEduTw()
cursos(datos,tabla)

tabla='CursosTsukubaAcJp'
datos=ObjBd.CursosOcwTsukubaAcJp()
cursos(datos,tabla)

tabla='CursosTudelftNl'
datos=ObjBd.cursosTudelftNl()
cursos(datos,tabla)

tabla='CursosTuftsEdu'
datos=ObjBd.cursosTuftsEdu()
cursos(datos,tabla)

tabla='CursosUabCat'
datos=ObjBd.CursosOcwUabCat()
cursos(datos,tabla)

tabla='CursosUaEs'
datos=ObjBd.CursosOcwUaEs()
cursos(datos,tabla)

tabla='CursosUaEs'
datos=ObjBd.CursosOcwUaEs()
cursos(datos,tabla)

tabla='CursosUc3m'
datos=ObjBd.cursosuc3()
cursos(datos,tabla)

tabla='CursosUc3m2'
datos=ObjBd.cursosuc3()
cursos(datos,tabla)

abla='CursosUc3m2'
datos=ObjBd.cursosuc3()
cursos(datos,tabla)

tabla='CursosUci'
datos=ObjBd.CursosOcwUci()
cursos(datos,tabla)

tabla='CursosUctAcZa'
datos=ObjBd.CursosOcwUctAcZa()
cursos(datos,tabla)

tabla='CursosUdemEduMx'
datos=ObjBd.CursosOcwUdemEduMx()
cursos(datos,tabla)

tabla='CursosUdlCat'
datos=ObjBd.cursosUdlCat()
cursos(datos,tabla)

tabla='CursosUgrEs'
datos=ObjBd.CursosOcwUgrEs()
cursos(datos,tabla)

tabla='CursosUibEs'
datos=ObjBd.CursosOcwUibEs()
cursos(datos,tabla)

tabla='CursosUmbEdu'
datos=ObjBd.CursosOcwUmbEdu()
cursos(datos,tabla)

tabla='CursosUmEs'
datos=ObjBd.CursosOcwUmEs()
cursos(datos,tabla)

tabla='CursosUmichEdu'
datos=ObjBd.CursosOcwUmichEdu()
cursos(datos,tabla)

tabla='CursosUnavEs'
datos=ObjBd.CursosOcwCursosUnavEs()
cursos(datos,tabla)

tabla='CursosUnedAcCr'
datos=ObjBd.CursosOcwUnedAcCr()
cursos(datos,tabla)

tabla='CursosUnicanEs'
datos=ObjBd.CursosOcwUnicanEs()
cursos(datos,tabla)

tabla='CursosUnioviEs'
datos=ObjBd.cursosUnioviEs()
cursos(datos,tabla)

tabla='CursosUnivalleEduCo'
datos=ObjBd.CursosOcwUnivalleEduCo()
cursos(datos,tabla)

tabla='CursosUnizarEs'
datos=ObjBd.CursosOcwUnizarEs()
cursos(datos,tabla)

tabla='CursosUnuEdu'
datos=ObjBd.CursosOcwUnuEdu()
cursos(datos,tabla)

tabla='CursosUocEdu'
datos=ObjBd.CursosOcwUocEdu()
cursos(datos,tabla)

tabla='CursosUpmEs'
datos=ObjBd.CursosOcwUpmEs()
cursos(datos,tabla)

tabla='CursosUpvEs'
datos=ObjBd.CursosOcwUpvEs()
cursos(datos,tabla)

tabla='CursosUpvEs'
datos=ObjBd.CursosOcwUpvEs()
cursos(datos,tabla)

tabla='CursosUsalEs'
datos=ObjBd.CursosOcwUsalEs()
cursos(datos,tabla)

tabla='scrapOcwUsEs'
datos=ObjBd.cursosocwus()
cursos(datos,tabla)

tabla='CursosUsuAcId'
datos=ObjBd.CursosOcwUsuAcId()
cursos(datos,tabla)

tabla='CursosUtmMy'
datos=ObjBd.CursosOcwUtmMy()
cursos(datos,tabla)

tabla='CursosUtplEduEc'
datos=ObjBd.CursosOcwUtplEduEc()
cursos(datos,tabla)

tabla='CursosUvEs'
datos=ObjBd.CursosOcwUvEs()
cursos(datos,tabla)

tabla='CursosLearnOpen'
datos=ObjBd.cursoslearnopen()
cursos(datos,tabla)"""