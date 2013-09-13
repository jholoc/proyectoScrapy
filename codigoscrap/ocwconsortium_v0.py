#-*-coding: utf-8 -*-
import re,string
from bs4 import *
from urllib import urlopen
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

urlscrap='http://www.ocwconsortium.org/en/members/members/master'
print urlscrap

webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear  
soup1 = BeautifulSoup(webpage1)
tiSoup = soup1.select("#pagecontent ul")#selecion de la pagina que contiene los titulos de las noticias
InicioPag='http://www.ocwconsortium.org'



for cont,i in enumerate(tiSoup):
    tituloBoque=i.previous_element.previous_element
    print tituloBoque
    liSoup=i.select('li')
    for universidades in liSoup:
        tituloUniverisdad=universidades.a.text.strip()
        urlUniversidad=InicioPag+universidades.a.get('href')
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
        print '        %s'%TituloUnive
        if contenido.select('img')!=[]:
            imagen=contenido.select('img')[0].get('src')
            print '        IMAGEN= %s'%InicioPag+imagen
        DescripUnive=contenido.text
        print '        TEXTO=%s ...'%DescripUnive[0:100].strip()#imprime una porcion de la descripcion
        #print '        %s'%DescripUnive#imprime toda la descripcion

        fieldset=contenidoUniversi[0].select('fieldset')
        for conta,fiel in enumerate(fieldset):
            tituloInformacion=fiel.legend.text
            titulodeurl=fiel.dd.text
            urlInformacion=fiel.dl.dt.a.get('href')
            print '        %s'%tituloInformacion
            print '            %s'%titulodeurl
            print '            %s'%urlInformacion

        tablacontenido=contenidoUniversi[0].select('#cfResultsTable')
        if tablacontenido!=[]:
            print '        si hay tabla'
            #print tablacontenido

            filastabla=tablacontenido[0].select('tbody > tr')
            for filas in filastabla:
                columnas=filas.select('td')
                
                cursotitulo=columnas[0].a.text
                linkcurso=columnas[0].a.get('href')
                detalles=columnas[1].a.text
                linkdetalle=InicioPag+columnas[1].a.get('href')
                lenguaje=columnas[2].text

                print'            Curso= %s -> %s'%(cursotitulo,linkcurso)
                print'            Detalles= %s -> %s'%(detalles,linkdetalle)
                print'            Lenguaje= -> %s'%lenguaje

                print 
 
                #print filas.text
                print '           ----------------'


        else:
            print '        no hay tabla'
        
        print'------------------------------------------------------'