#-*-coding: utf-8 -*-

import codecs
import nltk 
from nltk import *
import zipfile, re
from pyPdf import PdfFileReader
#import matplotlib.pyplot as plt

from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata

def insertbd(dat1, dat2, dat3):
    ObjBd = BDdatos()
    tabla = 'noticia'
    ObjBd.insertar_datos(dat1, dat2, dat3, tabla)
def insertbdtri(s, p, o):
    ObjBd = BDdatos()
    tabla = 'scrapy_ws'#'Tripleta'
    ObjBd.insertar_datos_trip(s, p, o, tabla)
def insertri(url, titulo, fecha, autor, textoCont,soup2,contok,titok,autok):
    #Envio de los datos a una base en forma de tripletas (s,p,o)
    insertbdtri(url, "url", url)        
    insertbdtri(url, "titulo", titulo)        
    insertbdtri(url, "fecha", fecha)        
    insertbdtri(url, "autor", autor)        
    insertbdtri(url, "contenido", textoCont)        
    insertbdtri(url, "contenidohtml", soup2)        
    insertbdtri(url, "contenidotoken", contok)        
    insertbdtri(url, "titulotoken", titok)        
    insertbdtri(url, "autortoken", autok)        
 
def word(url):
    docx = zipfile.ZipFile(url)
    content = docx.read('word/document.xml')
    cleaned = re.sub('<(.|\n)*?>','',content)
    print cleaned
    token=nltk.word_tokenize(cleaned)
    tag=nltk.pos_tag(token)
    print tag
    guardar = open('/home/andy/word.txt', 'w')
    for elem in tag:
        guardar.write(str(elem)+" ")
    guardar.close()

def pdfs(url):
        """EXTRAE PORCION DE TEXTO DE ARCHIVOS PDF"""
        archivo_pdf = PdfFileReader(file(url, "rb"))    #Capturar el archivo pdf a leer
        pagina = archivo_pdf.getPage(1)   #Capturar una pagina
        texto = pagina.extractText()  #Extrae el texto de la pagina capturada
        texto_listo= unicodedata.normalize('NFKD', texto).encode('ascii','ignore') #normaliza la codificacion del texto
        return(texto_listo)

def blogutpl(urlscrap): 
    webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear
    
    soup1 = BeautifulSoup(webpage1)
    #print soup1
    tiSoup = soup1.select("h2.title")#selecion de la pagina que contiene los titulos de las noticias
    #print "sadsa"
    #print tiSoup

    for i in tiSoup:    
        titulo = i.text #extracion del texto
        url = i.a.get('href') #extracion del link
        
        webpage2 = urlopen(url).read()  #leectura de la pagina obtenida de la extracion del link de la pagina anterior
        soup2 = BeautifulSoup(webpage2)
        Cont2Soup = soup2.select("div.postmeta-primary span")
        
        fecha = Cont2Soup[0].text #extracion de la fecha
        autor = Cont2Soup[1].text #extracion del autor     
        
        ContSoup = soup2.select("div.clearfix.entry p")        
        textoCont=""
        
        for j in ContSoup:
            textoCont =textoCont+j.text+"\n" #extracion del contenido de la noticias   
        
        
        print "----------------------------------------------------------------"                
        print "Url = ", url
        print "Titulo = ", titulo
        print "Fecha = ", fecha
        print "Autor = ", autor
        print "Texto = ", textoCont        
        print "----------------------------------------------------------------"
        
        texto_listo=unicodedata.normalize('NFKD', textoCont).encode('ascii','ignore') #Normalizacion del contenido
        titulo_listo=unicodedata.normalize('NFKD', titulo).encode('ascii','ignore') #Normalizacion del titulo
        autor_listo=unicodedata.normalize('NFKD', autor).encode('ascii','ignore') #Normalizacion del autor

        token=nltk.word_tokenize(texto_listo)       #Tokenizacion del texto, titulos, autores
        contok=str(nltk.pos_tag(token))
                
        token=nltk.word_tokenize(titulo_listo)
        titok=str(nltk.pos_tag(token))
        
        token=nltk.word_tokenize(autor_listo)
        autok=str(nltk.pos_tag(token))

        print autok
                
        #insertri(url, titulo, fecha, autor, textoCont,soup2,contok,titok,autok)  #Envio de datos a la funcion para enviarlo a tripeltas



nombre_archivo='http://www.utpl.edu.ec/comunicacion/page/1'

if nombre_archivo.split('.')[-1] == "pdf":        
    print "es un pdf"
    pdf(nombre_archivo)       
elif nombre_archivo.split('.')[-1] == "doc" or nombre_archivo.split('.')[-1] == "docx" or nombre_archivo.split('.')[-1] == "odt":
    print "es un word"
    word(nombre_archivo)
elif nombre_archivo.split('.')[-1] == "ppt":
    print "es una presentacion"            
elif nombre_archivo.split('.')[-1] == "xls":
    print "es un excel"
elif nombre_archivo.split('.')[-1] == "zip" or nombre_archivo.split('.')[-1] == "rar":
    print "es una zip o rar"
else:
    blogutpl(nombre_archivo)
    print "es un algo"
    


#for x in xrange(1,971):
#for x in xrange(1,2):
#    url='http://www.utpl.edu.ec/comunicacion/page/'+str(x)
#    blogutpl(url)