#-*-coding: utf-8 -*-
import re,string
from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def eliminasignos( text ):
    return re.sub('[%s]' % re.escape(string.punctuation), '', text)

def removersignos(text):
    signos=(',','.',';',':','+','{','}','[',']','(',')','^','~','#')
    for sig in signos:
        text=text.replace(sig,"")
    return text





#urlscrap='http://ocw.unizar.es/ocw/ensenanzas-tecnicas/fundamentos-de-informatica-grado-de-ingenieria-mecanica'

urlscrap='http://ocw.unizar.es/ocw/ensenanzas-tecnicas/vision-por-ordenador'


urlscrap='http://ocw.korea.edu/ocw/law-school/bbfcbc952'

webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear
    
soup1 = BeautifulSoup(webpage1)
#print soup1
tiSoup = soup1.select(".portletItem")#selecion de la pagina que contiene los titulos de las noticias
#print "sadsa"
#print tiSoup
for i in tiSoup:
    print i.a.text
    print i.a.get('href')
    urlmenu=i.a.get('href')
    webpage2=urlopen(urlmenu).read()
    soup2=BeautifulSoup(webpage2)
    #hrefs= soup2.select('a[href$=".pdf"]')
    #hrefs= soup2.findall(href=re.compile ('.pdf'))
    #hrefs= soup2.find_all(href=re.compile("\.(..)"))
    #hrefs= soup2.find_all(href=re.compile("\.(.{3,4},[^(org)])$"))
    hrefs= soup2.find_all(href=re.compile("\.(pdf|mp3|zip|tar|gz|html)$"))
    for href in hrefs:
    	aux=href.previous_element
        print len(aux)
        print aux
    	if len(aux)<6:
    		print 'PEQUEÑO'
    		aux=aux.previous_element.previous_element.previous_element.previous_element
        """while len(str(aux))<4:
            print 'AQIIIII'
            aux=aux.previous_element
            print aux"""
    	if str(aux)[0]=='<':
            if str(aux)[1]=='a':
                pass
            else:
                print '    %s'%aux.text#removersignos(aux.text)

    	else:
    		print '   %s'%aux#removersignos(aux)
    	#print '		%s'%href.previous_element.next_element
    	#print '		%s'%href
        print '            %s'%href.text
        print '            %s'%href.get('href')
