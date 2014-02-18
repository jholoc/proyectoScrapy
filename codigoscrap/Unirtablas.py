import re,string
from bs4 import *
from urllib import urlopen
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bd import *

tabla='OersUnidos'
#tabla='UnivesiaConsotiumUnidos'
ObjBd = BDdatos()
#ObjBd.crearTabla(tabla)
#sys.exit()
listatablas=['CursosAghEduPl','CursosAvuOrg','CursosIcesiEduCo','CursosInnovaUnedEs','CursosJhsphEdu','CursosKoreaEdu','CursosKyushuuAcJp','CursosLabspaceOpenAcUk','CursosLearnOpen','CursosMetropoliaFi','CursosMetuEduTr','CursosMit2','CursosNckuEduTw','CursosNdEdu','CursosNjitEdu','CursosNottinghamAcUk','CursosOpenLearn','CursosOpenmarhiRu','CursosSbuAcIr','CursosTmuEduTw','CursosTsukubaAcJp','CursosTudelftNl','CursosTuftsEdu','CursosUabCat','CursosUaEs','CursosUc3m2','CursosUci','CursosUctAcZa','CursosUdemEduMx','CursosUdlCat','CursosUgrEs','CursosUibEs','CursosUmbEdu','CursosUmEs','CursosUmichEdu','CursosUnavEs','CursosUnedAcCr','CursosUnicanEs','CursosUnioviEs','CursosUnivalleEduCo','CursosUniversia2','CursosUnizarEs','CursosUnuEdu','CursosUocEdu','CursosUpmEs','CursosUpvEs','CursosUsalEs','CursosUsEs','CursosUsuAcId','CursosUtmMy','CursosUtplEduEc','CursosUvEs','CursosVideoLectures']
#listatablas=['CursosUniversia2']
for tablacursos in listatablas:
	ObjBd.insertar_datos_trip_Tabla(tabla,tablacursos)	