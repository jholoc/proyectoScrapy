#-*-coding: utf-8 -*-
import re,string
from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

urlscrap='http://www.ocwconsortium.org/en/members/memberprofile/145'
urlscrap='http://www.ocwconsortium.org/en/members/memberprofile/18677'
print urlscrap

webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear  
soup1 = BeautifulSoup(webpage1)
tiSoup = soup1.select("#cfResultsTable")#selecion de la pagina que contiene los titulos de las noticias
print tiSoup[0]