#-*-coding: utf-8 -*-
import re,string
from bs4 import *
from urllib import urlopen
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
InicioPag='http://www.ocwconsortium.org'
urlscrap='http://www.ocwconsortium.org/members/all/'
webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear  
soup1 = BeautifulSoup(webpage1)
tiSoup = soup1.select(".columns.large-9 ul li")#selecion de la pagina que contiene los titulos de las noticias
for uni in tiSoup:
	tituloUniverisdad= InicioPag+uni.a.get('href')
	estrella=uni.a.select('i')
	if estrella!=[]:
            print '    #%s'%tituloUniverisdad
            print 'estrella'
        else:
            print '    %s'%tituloUniverisdad