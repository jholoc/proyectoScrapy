#-*-coding: utf-8 -*-
import re,string
from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def BuscaDescrip(aux):
    #aux=href.previous_element
    while len(str(aux).replace(' ',''))<=3 or str(aux)[0]=='<':
        if str(aux)[0]=='<':
            if str(aux)[1]=='a':
                break
            else:
                if str(aux)[1]=='t' or str(aux)[1]=='i':
                    aux=aux.previous_element
                else:
                    break
        else:
            aux=aux.previous_element

    if str(aux)[0]=='<':
        if str(aux)[1]=='a':
            pass
        else:
            htmlOer=aux.parent # html del oer
            descripOer=aux.text#removersignos(aux.text)
            #print '    %s'%descripOer

    else:
        htmlOer=aux.parent
        descripOer=aux#removersignos(aux)
        #print '   %s'%descripOer
    return descripOer

def unionurl(urlpag,urloer):
    if 'http://' in urloer:
        return urloer
    else:
        list1= urlpag.split('/')
        list2= urloer.split('/')
        list1.extend([element for element in list2 if element not in list1])
        union= '/'.join(list1)
        return union


urlscrap='http://www.ocwconsortium.org/en/members/members/master'
print urlscrap

webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear  
soup1 = BeautifulSoup(webpage1)
tiSoup = soup1.select("#pagecontent ul")#selecion de la pagina que contiene los titulos de las noticias
InicioPag='http://www.ocwconsortium.org'



for cont,i in enumerate(tiSoup):
    print BuscaDescrip (i.previous_element)
    print i.previous_element.previous_element
    liSoup=i.select('li')
    for universidades in liSoup:
        tituloUniverisdad=universidades.a.text.strip()
    	#urlUniversidad=unionurl(urlscrap,i.a.get('href'))
        urlUniversidad=InicioPag+universidades.a.get('href')
    	#urlUniversidad=universidades.a.get('href')
    	#print '    %s'%tituloUniverisdad
    	#print '    %s'%urlUniversidad
        estrella=universidades.next_element.next_element
        if str(estrella)[0]=='<' and str(estrella)[1]=='i':
            print '    #%s'%tituloUniverisdad
        else:
            print '    %s'%tituloUniverisdad
        print '    %s'%urlUniversidad


        webpage2 = urlopen(urlUniversidad).read() #lectura de la pagina a scrapear  
        soup2 = BeautifulSoup(webpage2)
        contenidoUniversi= soup2.select('div#pagecontent')
        TituloUnive=contenidoUniversi[0].h2.text.strip()
        contenido=contenidoUniversi[0].select('div.mpdescription')[0]
    	#print contenido.select('img')
        print '        %s'%TituloUnive
        if contenido.select('img')!=[]:
            imagen=contenido.select('img')[0].get('src')
            print '        IMAGEN= %s'%InicioPag+imagen
        DescripUnive=contenido.text
        print '        %s'%DescripUnive

        fieldset=contenidoUniversi[0].select('fieldset')
        for conta,fiel in enumerate(fieldset):
            print '        %s'%fiel.legend.text
        print'------------------------------------------------------'

