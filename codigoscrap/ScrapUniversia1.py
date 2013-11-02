# -*- coding: utf-8 -*-
import re,string,requests
from bs4 import *
from urllib import urlopen
from bd import *
import unicodedata
import sys
import urllib
reload(sys)
sys.setdefaultencoding("utf-8")


def eliminasignos( text ):
    text=eliminaNumeros(text)
    return re.sub('[%s]' % re.escape(string.punctuation), '', text)
def eliminaNumeros( text ):
    return re.sub('[%s]' % re.escape(string.digits), '', text)
def verificaUrl(url):
    if 'javascript:' in url:
        return False
    elif url.count('http:')>1:
        return False
    else:
        return True
    return True
def eliminaTags(soup1,tag):
    for trtagg in soup1.find_all(tag):
        #print trtagg
        trtagg.unwrap()

def removersignos(text):
    signos=(',','.',';','+','{','}','[',']','(',')','^','~','#')
    for sig in signos:
        text=text.replace(sig,"")
    return text

def unionurl(urlpag,urloer):
    if 'http://' in urloer or 'https://' in urloer:
        if 'view.php?id=' in urloer:    
            return urloer+'&redirect=1'
        return urloer
    else:
        if urlpag[len(urlpag)-1]=='/':
            urlpag=urlpag[0:len(urlpag)-1]
        list1= urlpag.strip().split('/')
        list2= urloer.strip().split('/')
        list1.extend([element for element in list2 if element not in list1])
        union= '/'.join(list1)
        return union
def extraernombremenu(urlmenu):
    url=urlmenu.split('/')
    if url[len(url)-1]!='':
        return url[len(url)-1]
    else:
        return url[len(url)-2]

def extraerextoer(urlmenu):
    url=urlmenu.split('.')
    return url[len(url)-1]
def identificarOer(url):
    if identificarOer2(url)=='0':
        #print 'if'
        print url
        url=requests.get(url).url
        return identificarOer2(url)
    else:
        #print 'else'
        return identificarOer2(url)

def identificarOer2(url):
    patron = re.compile("(\.(pdf|mp3|mp4|wmv|zip|rar|tar|gz|htm|xls|xlsx|doc|docx|odt|pps|ppt|pptx|XLS|DOCX|PPTX|jpg|gif|ISO|iso|epv|mobipocket|swf|jar)$)")
    if "http://www.youtube.com/watch" in url:
        return'video Youtube'
    busqueda=patron.search(url)
    try:
        if busqueda==None:  
            urlOpen=urllib.urlopen(url)
            infoUrl=urlOpen.info()['Content-Type']
            #print infoUrl
            if infoUrl=='application/pdf':
                return 'pdf'
            elif infoUrl=='application/zip':
                return 'zip'
            elif infoUrl=='application/octet-stream':
                return 'archivo binario de MIME'
            elif infoUrl=='application/rar':
                return 'rar'
            elif infoUrl=='application/msword':
                return 'dot'
            elif infoUrl=='application/pdf;charset=UTF-8':
                return 'pdf'
            elif infoUrl=='image/jpeg':
                return 'jpeg'
            else:
                return '0'
    except Exception, e:
            return '0'
def EncuentraDescripcion(aux):
    while len(str(aux).replace(' ','').strip())<=10 or str(aux)[0]=='<':
        if str(aux)[0]=='<':
            if str(aux)[1]=='a':
                aux=aux.previous_element
                #break
            else:
                if str(aux)[1]=='i' or str(aux)[1]=='p' or str(aux)[1]=='s' or str(aux)[1]=='e' or (str(aux)[1]=='t' and str(aux)[2]=='d'):
                    aux=aux.previous_element
                else:
                    break
        else:
            aux=aux.previous_element
        #print '------------------'
        #print aux

    if str(aux)[0]=='<':
        if str(aux)[1]=='a':
            pass
        else:
            htmlOer=aux.parent # html del oer
            descripOer=removersignos(aux.text).strip()#aux.text
            #print '    %s'%descripOer

    else:
        htmlOer=aux.parent
        descripOer=removersignos(aux).strip()#aux
        #print '   %s'%descripOer

    return [descripOer,htmlOer]


def ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido):
    continuar=True
    urlscrap=UrlCurso
    print '%s'%(urlscrap)
  
    ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)#insertar en la bd Link
    ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type
    try:
        if 'http://ocw.ua.es' in urlscrap:
            webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear
            soup1 = BeautifulSoup(webpage1)

            urlscrap2 = soup1.select("script")[0].text.split('"')[1]#abrir la redireccion 

            print '%s'%(urlscrap2) 
            webpage1 = urlopen(urlscrap2).read() #lectura de la pagina a scrapear
            soup1 = BeautifulSoup(webpage1)
        else:
            #webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear 
            #webpage1 = webpage1.replace('<p>','').replace('</p>','').replace('<br>','')
            url=requests.get(urlscrap).text
            soup1 = BeautifulSoup(url)
    except Exception, e:
        print e
        continuar=False
    
    if continuar==True:
        eliminaTags(soup1,'td')
        eliminaTags(soup1,'span')
        eliminaTags(soup1,'img')

        htmlCurso = soup1.select(estructuraContenido[0])# '.mwc_contenido'  html del curso

        if htmlCurso==[]:
            htmlCurso = soup1.select(estructuraContenido[1])#  '#content' html del curso
        if htmlCurso==[]: 
            ObjBd.insertar_datos_trip(urlscrap,'html',str(htmlCurso[0]),tabla)
        if htmlCurso!=[]:
            hrefs= htmlCurso[0].find_all('a', href=True)
            for href in hrefs:
                list1=urlscrap.split('/')[0:3]
                urlsimple='/'.join(list1)
                urlOer=unionurl(urlsimple,href.get('href'))
                #print urlOer
                try:
                    extoer=identificarOer(urlOer)
                except Exception, e:
                    continue
                
                if extoer=='0':
                    continue
                
                print '    %s'%urlOer
                decripOer=EncuentraDescripcion(href.previous_element)
                textoOer=href.text
                descripOer=decripOer[0]
                htmlOer=decripOer[1]
                
                ObjBd.insertar_datos_trip(urlscrap,'oer',urlOer,tabla)
                ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
                ObjBd.insertar_datos_trip(urlOer,'title',descripOer ,tabla)
                ObjBd.insertar_datos_trip(urlOer,'description',textoOer,tabla)
                ObjBd.insertar_datos_trip(urlOer,'html',str(htmlOer),tabla)
                ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
                ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)

def ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido):
    continuar=True
    urlscrap=UrlCurso
    print '%s'%(urlscrap)
    ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)#insertar en la bd Link
    ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type
    try:
        webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear 
        webpage1 = webpage1.replace('<p>','').replace('</p>','').replace('<br>','')
        soup1 = BeautifulSoup(webpage1)
        tiSoup = soup1.select(estructuraContenido[0])# "table.upv_lista"  selecion de la pagina que contiene los titulos de las noticias
    except Exception, e:
        print e
        continuar=False
    
    if continuar==True:
        for i in tiSoup:
            tituloMenu=i.text.strip()
            urlMenu=unionurl(urlscrap,i.get('href'))
            
            ObjBd.insertar_datos_trip(urlscrap,'menu',urlMenu,tabla)
            ObjBd.insertar_datos_trip(urlMenu,'link',urlMenu,tabla)
            ObjBd.insertar_datos_trip(urlMenu,'title',tituloMenu,tabla)
            ObjBd.insertar_datos_trip(urlMenu,'rdf:type','menu',tabla)
            nombreMenu=extraernombremenu(urlMenu)
            ObjBd.insertar_datos_trip(urlMenu,'rdf:type',nombreMenu,tabla)
            
            #print tituloMenu
            print '    %s'%urlMenu
            try:
                urlMenu= unicodedata.normalize('NFKD', urlMenu).encode('ascii','ignore')
                webpage2=urlopen(urlMenu).read()
                #webpage2 = webpage2.replace('<p>','').replace('</p>','')
            except Exception, e:
                print e
                continue
            
            soup2=BeautifulSoup(webpage2)
            htmlCurso = soup2.select(estructuraContenido[1])# '.mwc_contenido'  html del curso

            if htmlCurso==[]:
                htmlCurso = soup2.select(estructuraContenido[2])#  '#content' html del curso
            if htmlCurso==[]:
                continue

            ObjBd.insertar_datos_trip(urlMenu,'html',str(htmlCurso),tabla)
            hrefs= htmlCurso[0].find_all('a', href=True)
            for href in hrefs:
                try:
                    if verificaUrl(href.get('href'))==False:
                        continue
                    list1=urlscrap.split('/')[0:3]
                    urlsimple='/'.join(list1)
                    if href.get('href')[0]!='/':
                        urlOer=unionurl(urlscrap,href.get('href'))
                    else:
                        urlOer=unionurl(urlsimple,href.get('href'))

                    patron = re.compile("/view$")
                    busqueda=patron.search(urlOer)
                    textoOer=''
                    if busqueda!=None:
                        webpage3=urlopen(urlOer).read()
                        soup3=BeautifulSoup(webpage3)
                        htmlOerView = soup3.select('#region-content')
                        textoOer=htmlOerView[0].select('h1')[0].text
                        if textoOer=='Lo sentimos, pero la página no existe…':
                            urlOer=unionurl(urlscrap,href.get('href'))
                            webpage3=urlopen(urlOer).read()
                            soup3=BeautifulSoup(webpage3)
                            htmlOerView = soup3.select('#region-content')
                            textoOer=htmlOerView[0].select('h1')[0].text
                        #urlOer=htmlOerView[0].select ('.objectMetadata')
                        urlOer=htmlOerView[0].select('p > a')[0].get('href') #find_all('a', href=True)[4].get('href')
                        urlOer=unionurl(urlscrap,urlOer)
                
                    extoer=identificarOer(urlOer)
                except Exception, e:

                    continue
                
                if extoer=='0':
                    continue
                
                print '        %s'%urlOer
                decripOer=EncuentraDescripcion(href.previous_element)
                if textoOer=='':
                    textoOer=href.text
                descripOer=decripOer[0]
                htmlOer=decripOer[1]
                
                ObjBd.insertar_datos_trip(urlMenu,'oer',urlOer,tabla)
                ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
                ObjBd.insertar_datos_trip(urlOer,'title',descripOer ,tabla)
                ObjBd.insertar_datos_trip(urlOer,'description',textoOer,tabla)
                ObjBd.insertar_datos_trip(urlOer,'html',str(htmlOer),tabla)
                ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
                ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)



#www.upv.es
def ScrapUpvEs(UrlCurso,tabla):#no hay como scpraear
    print 'Error al Scrapear'
    ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)
#www.unsavirtual.edu.pe:8090
def ScrapUnsavirtualEduPe8090(UrlCurso,tabla):#no hay como scpraear
    print 'FUERA DE LINEA'
    ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
#www.unav.es
def ScrapUanvEs(UrlCurso,tabla):
    estructuraContenido=['td.menu_asignatura > a','td.contenido','td.contenido']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#www.uhu.es
def ScrapUhuEs(UrlCurso,tabla):#www.uhu.es
    estructuraContenido=['div.templatemo_leftmenu > a','div#templatemo_right_mid','div#templatemo_right_mid']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#www.ocw.unc.edu.ar
def ScrapUncEduAr(UrlCurso,tabla):#www.ocw.unc.edu.ar
    estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','div#parent-fieldname-text','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#www.lapetus.uchile.cl
def ScrapUchileCl(UrlCurso,tabla):#no hay como scpraear
    #estructuraContenido=['div#programa','div#main']
    #ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    print 'Error al Scrapear'
    ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)
#www.icesi.edu.co
def ScrapIcesiEduCo(UrlCurso,tabla):#www.icesi.edu.co
    estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocwus.us.es
def ScrapUsEs(UrlCurso,tabla):
    estructuraContenido=['div.unSelected > a','#region-content','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocwbeta.uji.es   
def ScrapUjiEs(UrlCurso,tabla):
    estructuraContenido=['div#mainContent','#main']
    ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
#ocw.virtualum.edu.co
def ScrapVirtualumEduCo(UrlCurso,tabla):#no hay como scpraear
    print 'FUERA DE LINEA'
    ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
#ocw.uv.es
def ScrapUvEs(UrlCurso,tabla):
    estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','.plain','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.usc.es
def ScrapUscEs(UrlCurso,tabla):
    print 'FUERA DE LINEA'
    ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
#ocw.usal.es
def ScrapUsalEs(UrlCurso,tabla):
    estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelecte > a','.plain','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.upm.es
def ScrapUpmEs(UrlCurso,tabla):
    estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.upc.edu
def ScrapUpcEdu(UrlCurso,tabla):
    estructuraContenido=['div#block-ocw-0 > div > div > ul > li > a','#content-region','#content-group']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.uoc.edu
def ScrapUocEdu(UrlCurso,tabla): 
    estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','div.plain','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.unizar.es
def ScrapUnizarEs(UrlCurso,tabla): #ocw.unizar.es
    estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','div.plain','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)   
#ocw.univalle.edu.co
def ScrapUnivalleEduCo(UrlCurso,tabla):
    estructuraContenido=['#portlet-eduCommonsNavigation > div.unSelected > a','.plain','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.uniovi.es
def ScrapUnioviEs(UrlCurso,tabla):#No permite obtener estructura, no aparece el menu
    #estructuraContenido=['div.webfx-tree-item > a','.content','#middle-column']
    #ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    print 'Error al Scrapear'
    ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)
#ocw.unican.es
def ScrapUnicanEs(UrlCurso,tabla):
    estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.unia.es
def ScrapUniaEs(UrlCurso,tabla): 
    estructuraContenido=['#portal-column-two','.portletReuseCourse']
    ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)

#ocw.uni.edu.pe
def ScrapUniEduPe(UrlCurso,tabla):
    estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','div.plain','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.umh.es
def ScrapUmhEs(UrlCurso,tabla):
    estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.uma.es
def ScrapUmaEs(UrlCurso,tabla):
    estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.um.es
def ScrapUmEs(UrlCurso,tabla):
    estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.ull.es
def ScrapUllEs(UrlCurso,tabla):#no hay como scpraear
    print 'FUERA DE LINEA'
    ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
#ocw.uis.edu.co
def ScrapUisEduCo(UrlCurso,tabla):
    estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#portal-column-content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.uib.es
def ScrapUibEs(UrlCurso,tabla):
    estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#portal-column-content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.ugr.es
def ScrapUgrEs(UrlCurso,tabla):
    estructuraContenido=['.topics','#middle-column']
    ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
#ocw.udl.cat
def ScrapUdlCat(UrlCurso,tabla):
    estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#portal-column-content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.udem.edu.mx
def ScrapUdemEduMx(UrlCurso,tabla):
    estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','.plain','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.uca.es
def ScrapUcaEs(UrlCurso,tabla):
    estructuraContenido=['#region-main','#region-main']
    ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
#ocw.uc3m.es
def ScrapUc3mEs(UrlCurso,tabla):
    estructuraContenido=['.portletItem > a','#parent-fieldname-text','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.uam.es
def ScrapUamEs(UrlCurso,tabla):
    estructuraContenido=['ul#navlist > div   > a','#id1','#main']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.ua.es
def ScrapUaEs(UrlCurso,tabla):
    estructuraContenido=['#cuerpo','#cuerpo']
    ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
#ocw.pucv.cl
def ScrapPucvCl(UrlCurso,tabla):
    estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.itesm.mx
def ScrapItesmMx(UrlCurso,tabla):
    print 'FUERA DE LINEA'
    ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
#ocw.innova.uned.es
def ScrapInnovaUnedEs(UrlCurso,tabla):
    estructuraContenido=['#portlet-eduCommonsNavigation > div.unSelected > a','.plain','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.ie.edu
def ScrapInnovaUnedEs(UrlCurso,tabla):
    estructuraContenido=['#portlet-eduCommonsNavigation > div.unSelected > a','.plain','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.flacso.edu.mx:8080
def ScrapFlacsoEduMx8080(UrlCurso,tabla):
    estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.ehu.es
def ScrapEhuEs(UrlCurso,tabla):
    print 'Error al Scrapear'
    """print UrlCurso
    webpage1=requests.get(UrlCurso).text
    #webpage1 = urlopen(url).read() #lectura de la pagina a scrapear 
    soup1 = BeautifulSoup(webpage1)
    try:
        linkSoup = soup1.select('#section-1 > td > ul > li a')[0].get('href')
        print linkSoup
    except Exception, e:
        print e
    
    #print soup1
    webpage1=requests.get(linkSoup).text
    soup1 = BeautifulSoup(webpage1)
    try:
        linkSoup = soup1.select('#content > div > a')[0].get('href')
        print linkSoup
    except Exception, e:
        print e
    webpage1=requests.get(linkSoup).url
    print webpage1
    estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','#region-content','#content']
    ScrapPaginasConMenu(webpage1,tabla,estructuraContenido)"""
#ocw.ceu.es
def ScrapCeuEs(UrlCurso,tabla):
    estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.camins.upc.edu
def ScrapCaminsUpcEdu(UrlCurso,tabla):
    estructuraContenido=['div.menuEsquerre > ul > li > a','div.span-20.last.prepend-1','div.span-20.last.prepend-1']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
#ocw.bib.upct.es
def ScrapBibUpctEs(UrlCurso,tabla):
    estructuraContenido=['li.depth_3 > p > a','#section-5','.course-content']
    ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)

def ScrapUniverdidades(linkOcw,tabla):
    Univeridad=linkOcw
    try:
        Univeridad= linkOcw.split('/')[2]
    except Exception, e:
        print 'Url Incorrecta %s'%linkOcw

    if Univeridad == 'www.upv.es':
        ScrapUpvEs(linkOcw,tabla)
    elif Univeridad == 'www.unsavirtual.edu.pe:8090':
        ScrapUnsavirtualEduPe8090(linkOcw,tabla)
    elif Univeridad == 'www.unav.es':
        ScrapUanvEs(linkOcw,tabla)
    elif Univeridad == 'www.uhu.es':
        ScrapUhuEs(linkOcw,tabla)
    elif Univeridad == 'www.ocw.unc.edu.ar':
        ScrapUncEduAr(linkOcw,tabla)
    elif Univeridad == 'www.lapetus.uchile.cl':
        ScrapUchileCl(linkOcw,tabla)
    elif Univeridad == 'www.icesi.edu.co':
        ScrapIcesiEduCo(linkOcw,tabla)
    elif Univeridad == 'ocwus.us.es':
        ScrapUsEs(linkOcw,tabla)
    elif Univeridad == 'ocwbeta.uji.es':
        ScrapUjiEs(linkOcw,tabla)
    elif Univeridad == 'ocw.virtualum.edu.co':
        ScrapVirtualumEduCo(linkOcw,tabla)
    elif Univeridad == 'ocw.uv.es':
        ScrapUvEs(linkOcw,tabla)
    elif Univeridad == 'ocw.usc.es':
        ScrapUscEs(linkOcw,tabla)
    elif Univeridad == 'ocw.usal.es':
        ScrapUsalEs(linkOcw,tabla)
    elif Univeridad == 'ocw.upm.es':
        ScrapUpmEs(linkOcw,tabla)
    elif Univeridad == 'ocw.upc.edu':
        ScrapUpcEdu(linkOcw,tabla)
    elif Univeridad == 'ocw.uoc.edu':
        ScrapUocEdu(linkOcw,tabla)
    elif Univeridad == 'ocw.unizar.es':
        ScrapUnizarEs(linkOcw,tabla)
    elif Univeridad == 'ocw.univalle.edu.co':
        ScrapUnivalleEduCo(linkOcw,tabla)
    elif Univeridad == 'ocw.uniovi.es':
        ScrapUnioviEs(linkOcw,tabla)
    elif Univeridad == 'ocw.unican.es':
        ScrapUnicanEs(linkOcw,tabla)
    elif Univeridad == 'ocw.unia.es':
        ScrapUniaEs(linkOcw,tabla)
    elif Univeridad == 'ocw.uni.edu.pe':
        ScrapUniEduPe(linkOcw,tabla)
    elif Univeridad == 'ocw.umh.es':
        ScrapUmhEs(linkOcw,tabla)
    elif Univeridad == 'ocw.uma.es':
        ScrapUmaEs(linkOcw,tabla)
    elif Univeridad == 'ocw.um.es':
        ScrapUmEs(linkOcw,tabla)
    elif Univeridad == 'ocw.ull.es':
        ScrapUllEs(linkOcw,tabla)
    elif Univeridad == 'ocw.uis.edu.co':
        ScrapUisEduCo(linkOcw,tabla)
    elif Univeridad == 'ocw.uib.es':
        ScrapUibEs(linkOcw,tabla)
    elif Univeridad == 'ocw.ugr.es':
        ScrapUgrEs(linkOcw,tabla)
    elif Univeridad == 'ocw.udl.cat':
        ScrapUdlCat(linkOcw,tabla)
    elif Univeridad == 'ocw.udem.edu.mx':
        ScrapUdemEduMx(linkOcw,tabla)
    elif Univeridad == 'ocw.uca.es':
        ScrapUcaEs(linkOcw,tabla)
    elif Univeridad == 'ocw.uc3m.es':
        ScrapUc3mEs(linkOcw,tabla)
    elif Univeridad == 'ocw.uam.es':
        ScrapUamEs(linkOcw,tabla)
    elif Univeridad == 'ocw.ua.es':
        ScrapUaEs(linkOcw,tabla)
    elif Univeridad == 'ocw.pucv.cl':
        ScrapPucvCl(linkOcw,tabla)
    elif Univeridad == 'ocw.itesm.mx':
        ScrapItesmMx(linkOcw,tabla)
    elif Univeridad == 'ocw.innova.uned.es':
        ScrapInnovaUnedEs(linkOcw,tabla)
    elif Univeridad == 'ocw.ie.edu':
        ScrapInnovaUnedEs(linkOcw,tabla)
    elif Univeridad == 'ocw.flacso.edu.mx:8080':
        ScrapFlacsoEduMx8080(linkOcw,tabla)
    elif Univeridad == 'ocw.ehu.es':
        ScrapEhuEs(linkOcw,tabla)
    elif Univeridad == 'ocw.ceu.es':
        ScrapCeuEs(linkOcw,tabla)
    elif Univeridad == 'ocw.camins.upc.edu':
        ScrapCaminsUpcEdu(linkOcw,tabla)
    elif Univeridad == 'ocw.bib.upct.es':
        ScrapBibUpctEs(linkOcw,tabla)
    else:
        print 'no existe universidad %s'%Univeridad


tabla='CursosUniversia2'
#tabla='prueba'
ObjBd = BDdatos()

#ObjBd.crearTabla(tabla)
#sys.exit()
datos=ObjBd.CursosUniversia()

for cont,urlcurso in enumerate(datos):
    if cont<1375:
        continue
    url=urlcurso[0]
    print cont
    ScrapUniverdidades(url,tabla)

