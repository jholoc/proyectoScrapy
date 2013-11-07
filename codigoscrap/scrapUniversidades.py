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
ObjBd = BDdatos()
class Scrap():
        
    def eliminasignos(self,text ):
        text=self.eliminaNumeros(text)
        return re.sub('[%s]' % re.escape(string.punctuation), '', text)
    def eliminaNumeros(self,text ):
        return re.sub('[%s]' % re.escape(string.digits), '', text)
    def verificaUrl(self,url):
        if 'javascript:' in url:
            return False
        elif url.count('http:')>1:
            return False
        else:
            return True
        return True
    def eliminaTags(self,soup1,tag):
        for trtagg in soup1.find_all(tag):
            #print trtagg
            trtagg.unwrap()

    def removersignos(self,text):
        signos=(',','.',';','+','{','}','[',']','(',')','^','~','#')
        for sig in signos:
            text=text.replace(sig,"")
        return text

    def unionurl(self,urlpag,urloer):
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
    def extraernombremenu(self,urlmenu):
        url=urlmenu.split('/')
        if url[len(url)-1]!='':
            return url[len(url)-1]
        else:
            return url[len(url)-2]

    def extraerextoer(self,urlmenu):
        url=urlmenu.split('.')
        return url[len(url)-1]
    def identificarOer(self,url):
        if self.identificarOer2(url)=='0':
            #print 'if'
            url=requests.get(url).url
            return self.identificarOer2(url)
        else:
            #print 'else'
            return self.identificarOer2(url)

    def identificarOer2(self,url):
        patron = re.compile("(\.(pdf|mp3|mp4|mov|wmv|zip|rar|tar|gz|htm|xls|xlsx|doc|docx|odt|pps|ppt|pptx|XLS|DOCX|PPTX|jpg|gif|ISO|iso|epv|mobipocket|swf|jar|avi|AVI |txt|mpg)$)")
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
                elif infoUrl=='image/jpeg':
                    return 'jpeg'   
                elif infoUrl=='application/pdf;charset=UTF-8':
                    return 'pdf'
                elif infoUrl=='video/x-ms-wmv':
                    return 'wmv'
                elif infoUrl=='video/x-ms-asf':
                    return 'asf'
                else:
                    return '0'
            else:
                return self.extraerextoer(url)
        except Exception, e:
                return '0'
    def EncuentraDescripcion(self,aux):
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
                descripOer=self.removersignos(aux.text).strip()#aux.text
                #print '    %s'%descripOer

        else:
            htmlOer=aux.parent
            descripOer=self.removersignos(aux).strip()#aux
            #print '   %s'%descripOer

        return [descripOer,htmlOer]


    def ScrapPaginasSinMenu(self,UrlCurso,tabla,estructuraContenido):
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
            self.eliminaTags(soup1,'td')
            self.eliminaTags(soup1,'span')
            self.eliminaTags(soup1,'img')

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
                    urlOer=self.unionurl(urlsimple,href.get('href'))
                    #print urlOer
                    try:
                        extoer=self.identificarOer(urlOer)
                    except Exception, e:
                        continue
                    
                    if extoer=='0':
                        continue
                    
                    print '    %s'%urlOer
                    decripOer=self.EncuentraDescripcion(href.previous_element)
                    textoOer=href.text
                    descripOer=decripOer[0]
                    htmlOer=decripOer[1]
                    if descripOer=='':
                        descripOer=textoOer
                    elif textoOer=='':
                        textoOer=descripOer
                    
                    ObjBd.insertar_datos_trip(urlscrap,'oer',urlOer,tabla)
                    ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
                    ObjBd.insertar_datos_trip(urlOer,'title',descripOer ,tabla)
                    ObjBd.insertar_datos_trip(urlOer,'description',textoOer,tabla)
                    ObjBd.insertar_datos_trip(urlOer,'html',str(htmlOer),tabla)
                    ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
                    ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)

    def ScrapPaginasConMenu(self,UrlCurso,tabla,estructuraContenido):
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
                urlMenu=self.unionurl(urlscrap,i.get('href'))
                
                ObjBd.insertar_datos_trip(urlscrap,'menu',urlMenu,tabla)
                ObjBd.insertar_datos_trip(urlMenu,'link',urlMenu,tabla)
                ObjBd.insertar_datos_trip(urlMenu,'title',tituloMenu,tabla)
                ObjBd.insertar_datos_trip(urlMenu,'rdf:type','menu',tabla)
                nombreMenu=self.extraernombremenu(urlMenu)
                ObjBd.insertar_datos_trip(urlMenu,'rdf:type',nombreMenu,tabla)
                
                #print tituloMenu
                print '    %s'%urlMenu
                urlMenu= unicodedata.normalize('NFKD', urlMenu).encode('ascii','ignore')
                webpage2=urlopen(urlMenu).read()
                #webpage2 = webpage2.replace('<p>','').replace('</p>','')
                webpage2=requests.get(urlMenu).text
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
                        if self.verificaUrl(href.get('href'))==False:
                            continue
                        list1=urlscrap.split('/')[0:3]
                        urlsimple='/'.join(list1)
                        if href.get('href')[0]!='/':
                            urlOer=self.unionurl(urlscrap,href.get('href'))
                        else:
                            urlOer=self.unionurl(urlsimple,href.get('href'))

                        patron = re.compile("/(view.php|view)$")
                        busqueda=patron.search(urlOer)
                        textoOer=''
                        if busqueda!=None:
                            webpage3=urlopen(urlOer).read()
                            soup3=BeautifulSoup(webpage3)
                            htmlOerView = soup3.select('#region-content')
                            textoOer=htmlOerView[0].select('h1')[0].text
                            if textoOer=='Lo sentimos, pero la página no existe…':
                                urlOer=self.unionurl(urlscrap,href.get('href'))
                                webpage3=urlopen(urlOer).read()
                                soup3=BeautifulSoup(webpage3)
                                htmlOerView = soup3.select('#region-content')
                                textoOer=htmlOerView[0].select('h1')[0].text
                            #urlOer=htmlOerView[0].select ('.objectMetadata')
                            urlOer=htmlOerView[0].select('p > a')[0].get('href') #find_all('a', href=True)[4].get('href')
                            urlOer=self.unionurl(urlscrap,urlOer)
                    
                        extoer=self.identificarOer(urlOer)
                    except Exception, e:
                        print e
                    
                    if extoer=='0':
                        continue
                    
                    print '        %s'%urlOer
                    decripOer=self.EncuentraDescripcion(href.previous_element)
                    if textoOer=='':
                        textoOer=href.text
                    descripOer=decripOer[0]
                    htmlOer=decripOer[1]
                    if descripOer=='':
                        descripOer=textoOer
                    elif textoOer=='':
                        textoOer=descripOer
                    
                    ObjBd.insertar_datos_trip(urlMenu,'oer',urlOer,tabla)
                    ObjBd.insertar_datos_trip(urlOer,'link',urlOer,tabla)
                    ObjBd.insertar_datos_trip(urlOer,'title',descripOer ,tabla)
                    ObjBd.insertar_datos_trip(urlOer,'description',textoOer,tabla)
                    ObjBd.insertar_datos_trip(urlOer,'html',str(htmlOer),tabla)
                    ObjBd.insertar_datos_trip(urlOer,'rdf:type','oer',tabla)
                    ObjBd.insertar_datos_trip(urlOer,'rdf:type',extoer,tabla)
    def ScrapUci(self,urlscrap,tabla):
        print '%s'%(urlscrap)  
        ObjBd.insertar_datos_trip(urlscrap,'link',urlscrap,tabla)#insertar en la bd Link
        ObjBd.insertar_datos_trip(urlscrap,'rdf:type','ocw',tabla)#insertar en la bd type

        webpage1 = urlopen(urlscrap).read() #lectura de la pagina a scrapear 
        soup1 = BeautifulSoup(webpage1)
        htmlcurso=soup1.select('div.columnleft_nomiddle')
        ViSoup = soup1.select('iframe')

        ObjBd.insertar_datos_trip(urlscrap,'html',str(htmlcurso),tabla)


        if ViSoup != []:
            urlvi=ViSoup[0].get('src')
            if urlvi.find('embed/')<0:
                pass
            else:
                urlvi=urlvi.replace('embed/','watch?v=')

                webpage2=urlopen(urlvi).read()
                soup2=BeautifulSoup(webpage2)
                titulosoup = soup2.select('#eow-title')
                titulo=titulosoup[0].text
                descipcionsoup= soup2.select('#eow-description')
                descipcion= descipcionsoup[0].text

                ObjBd.insertar_datos_trip(urlscrap,'oer',urlvi,tabla)
                ObjBd.insertar_datos_trip(urlvi,'link',urlvi,tabla)
                ObjBd.insertar_datos_trip(urlvi,'title',titulo ,tabla)
                ObjBd.insertar_datos_trip(urlvi,'description',descipcion,tabla)
                ObjBd.insertar_datos_trip(urlvi,'html',str(webpage2),tabla)

                ObjBd.insertar_datos_trip(urlvi,'rdf:type','oer',tabla)
                ObjBd.insertar_datos_trip(urlvi,'rdf:type','video',tabla)


    #www.upv.es
    def ScrapUpvEs(self,UrlCurso,tabla):#no hay como scpraear
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)
    #www.unsavirtual.edu.pe:8090
    def ScrapUnsavirtualEduPe8090(self,UrlCurso,tabla):#no hay como scpraear
        print 'FUERA DE LINEA'
        ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
    #www.unav.es
    def ScrapUanvEs(self,UrlCurso,tabla):
        estructuraContenido=['td.menu_asignatura > a','td.contenido','td.contenido']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #www.uhu.es
    def ScrapUhuEs(self,UrlCurso,tabla):#www.uhu.es
        estructuraContenido=['div.templatemo_leftmenu > a','div#templatemo_right_mid','div#templatemo_right_mid']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #www.ocw.unc.edu.ar
    def ScrapUncEduAr(self,UrlCurso,tabla):#www.ocw.unc.edu.ar
        estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','div#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #www.lapetus.uchile.cl
    def ScrapUchileCl(self,UrlCurso,tabla):#no hay como scpraear
        #estructuraContenido=['div#programa','div#main']
        #ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)

    #www.icesi.edu.co
    def ScrapIcesiEduCo(self,UrlCurso,tabla):#www.icesi.edu.co
        estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocwus.us.es
    def ScrapUsEs(self,UrlCurso,tabla):
        estructuraContenido=['div.unSelected > a','#region-content','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocwbeta.uji.es   
    def ScrapUjiEs(self,UrlCurso,tabla):
        estructuraContenido=['div#mainContent','#main']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.virtualum.edu.co
    def ScrapVirtualumEduCo(self,UrlCurso,tabla):#no hay como scpraear
        print 'FUERA DE LINEA'
        ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
    #ocw.uv.es
    def ScrapUvEs(self,UrlCurso,tabla):
        estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','.plain','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.usc.es
    def ScrapUscEs(self,UrlCurso,tabla):
        print 'FUERA DE LINEA'
        ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
    #ocw.usal.es
    def ScrapUsalEs(self,UrlCurso,tabla):
        estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelecte > a','.plain','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.upm.es
    def ScrapUpmEs(self,UrlCurso,tabla):
        estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.upc.edu
    def ScrapUpcEdu(self,UrlCurso,tabla):
        estructuraContenido=['div#block-ocw-0 > div > div > ul > li > a','#content-region','#content-group']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.uoc.edu
    def ScrapUocEdu(self,UrlCurso,tabla): 
        estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','div.plain','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.unizar.es
    def ScrapUnizarEs(self,UrlCurso,tabla): #ocw.unizar.es
        estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','div.plain','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)   
    #ocw.univalle.edu.co
    def ScrapUnivalleEduCo(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-eduCommonsNavigation > div.unSelected > a','.plain','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.uniovi.es
    def ScrapUnioviEs(self,UrlCurso,tabla):#No permite obtener estructura, no aparece el menu
        #estructuraContenido=['div.webfx-tree-item > a','.content','#middle-column']
        #ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)
    #ocw.unican.es
    def ScrapUnicanEs(self,UrlCurso,tabla):
        estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.unia.es
    def ScrapUniaEs(self,UrlCurso,tabla): 
        estructuraContenido=['#portal-column-two','.portletReuseCourse']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)

    #ocw.uni.edu.pe
    def ScrapUniEduPe(self,UrlCurso,tabla):
        estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','div.plain','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.umh.es
    def ScrapUmhEs(self,UrlCurso,tabla):
        estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.uma.es
    def ScrapUmaEs(self,UrlCurso,tabla):
        estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.um.es
    def ScrapUmEs(self,UrlCurso,tabla):
        estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.ull.es
    def ScrapUllEs(self,UrlCurso,tabla):#no hay como scpraear
        print 'FUERA DE LINEA'
        ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
    #ocw.uis.edu.co
    def ScrapUisEduCo(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#portal-column-content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.uib.es
    def ScrapUibEs(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#portal-column-content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.ugr.es
    def ScrapUgrEs(self,UrlCurso,tabla):
        estructuraContenido=['.topics','#middle-column']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.udl.cat
    def ScrapUdlCat(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#portal-column-content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.udem.edu.mx
    def ScrapUdemEduMx(self,UrlCurso,tabla):
        estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','.plain','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.uca.es
    def ScrapUcaEs(self,UrlCurso,tabla):
        estructuraContenido=['#region-main','#region-main']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.uc3m.es
    def ScrapUc3mEs(self,UrlCurso,tabla):
        estructuraContenido=['.portletItem > a','#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.uam.es
    def ScrapUamEs(self,UrlCurso,tabla):
        estructuraContenido=['ul#navlist > div   > a','#id1','#main']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.ua.es
    def ScrapUaEs(self,UrlCurso,tabla):
        estructuraContenido=['#cuerpo','#cuerpo']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.pucv.cl
    def ScrapPucvCl(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.itesm.mx
    def ScrapItesmMx(self,UrlCurso,tabla):
        print 'FUERA DE LINEA'
        ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
    #ocw.innova.uned.es
    def ScrapInnovaUnedEs(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-eduCommonsNavigation > div.unSelected > a','.plain','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.ie.edu
    def ScrapIeEdu(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-eduCommonsNavigation > div.unSelected > a','.plain','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.flacso.edu.mx:8080
    def ScrapFlacsoEduMx8080(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.ehu.es
    def ScrapEhuEs(self,UrlCurso,tabla):
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)

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
    def ScrapCeuEs(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.camins.upc.edu
    def ScrapCaminsUpcEdu(self,UrlCurso,tabla):
        estructuraContenido=['div.menuEsquerre > ul > li > a','div.span-20.last.prepend-1','div.span-20.last.prepend-1']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.bib.upct.es
    def ScrapBibUpctEs(self,UrlCurso,tabla):
        estructuraContenido=['li.depth_3 > p > a','#section-5','.course-content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)

    #########################################################CONSORTIUM##########################################################
    #ocw.mit.edu
    def ScrapMitEdu(self,UrlCurso,tabla):
        estructuraContenido=['li. > a','#course_inner_section','#course_inner_section']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #openlearn.open.ac.uk
    def ScrapOpenAcUk(self,UrlCurso,tabla):
        estructuraContenido=['div.content > ul > li > a','','']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.uci.edu
    def ScrapUCiEdu(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','#middle-column','#middle-column']
        self.ScrapUci(UrlCurso,tabla)
    #opencontent.uct.ac.za   
    def ScrapUctAcZa(self,UrlCurso,tabla):
        estructuraContenido=['div.weblinks-linkview > a','body','body']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #unow.nottingham.ac.uk
    def ScrapNottinghamAcUk(self,UrlCurso,tabla):
        estructuraContenido=['.content-dl','.content-dl']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #oer.avu.org
    def ScrapAvuOrg(self,UrlCurso,tabla):
        estructuraContenido=['table.file-list.ds-table','table.file-list.ds-table']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.hokudai.ac.jp
    def ScraphokudaiAcJp(self,UrlCurso,tabla):
        estructuraContenido=['table.dd','table.dd']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #open.umich.edu
    def ScrapUmichEdu(self,UrlCurso,tabla):
        estructuraContenido=['ul.course-navigation > li.last > a','#content-area','#content-area']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.metu.edu.tr 
    def ScrapMetuEduTr(self,UrlCurso,tabla):
        estructuraContenido=['div.bb > div > table > tbody > tr > td > table > tbody > tr > td > a ','#page-content','#page-content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.jhsph.edu   
    def ScrapJhsphEdu(self,UrlCurso,tabla):
        estructuraContenido=['div#courseNav > ul > li > a','div.col2','div.col2']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.korea.edu   
    def ScrapKoreaEdu(self,UrlCurso,tabla):
        estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#content','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.tsukuba.ac.jp   
    def ScrapTsukubaAcJp(self,UrlCurso,tabla):
        estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','#content','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #open.agh.edu.pl
    def ScrapaghEduPl(self,UrlCurso,tabla):
        estructuraContenido=['#middle-column','#middle-column'] 
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #yct.ncku.edu.tw 
    def ScrapNckuEduTw(self,UrlCurso,tabla):
        estructuraContenido=['div.module-content','div.module-content']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.nd.edu  
    def ScrapNdEdu(self,UrlCurso,tabla):
        estructuraContenido=['dl#portlet-simple-nav dd.portletItem > a','#content','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.tufts.edu   
    def ScrapTuftsEdu(self,UrlCurso,tabla):
        estructuraContenido=['ul.course_categories > li.category > a','div.right_course','div.right_course']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.utm.my
    def ScrapUtmMy(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)

    #ocw.umb.edu 
    def ScrapUmbEdu(self,UrlCurso,tabla):
        estructuraContenido=['dl#portlet-simple-nav > dd.portletItem > a','#content','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #www5.fgv.br
    def ScrapFgvBr(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)

    #peer-news.blogspot.com  
    def ScrapPeernewsBlogspotCom(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)

    #feedproxy.google.com    
    def ScrapGoogleCom(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)

    #ocw.nctu.edu.tw
    def ScrapNctuEduTw(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'FUERA DE LINEA'
        ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
    #www.open-marhi.ru   
    def ScrapOpenmarhiRu(self,UrlCurso,tabla):
        estructuraContenido=['div.left_menu_item > a','#content','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #graduateschool.paristech.fr
    def ScrapParistechFr(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'FUERA DE LINEA'
        ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
    #ocw.tmu.edu.tw:8080 
    def ScrapTmuEduTw8080(self,UrlCurso,tabla):
        estructuraContenido=['div#portlet-eduCommonsNavigation > div.unSelected > a','#content','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #www.unav.es 
    def ScrapUnavEs(self,UrlCurso,tabla):
        estructuraContenido=['td.menu_asignatura > a','td.contenido','td.contenido']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.njit.edu    
    def ScrapNjitEdu(self,UrlCurso,tabla):
        estructuraContenido=['div.colright','div.colright']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.tudelft.nl
    def ScrapTudelftNl(self,UrlCurso,tabla):
        estructuraContenido=['div#contentMenu > ul > li > ul > li > a','#contentText','#contentText']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.unu.edu 
    def ScrapUnuEdu(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-eduCommonsNavigation > div.unSelected > a','#content','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #www.ocw.titech.ac.jp
    def ScrapTitechAcJp(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)

    #ocw.uab.cat 
    def ScrapUabCat(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#parent-fieldname-text']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.uned.ac.cr  
    def ScrapUnedAcCr(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.itesm.mx
    def ScrapItesmMx(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'FUERA DE LINEA'
        ObjBd.insertar_datos_trip(UrlCurso,'error','FUERA DE LINEA',tabla)
    #ocw.ie.edu  
    def ScrapIeEdu(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)

    #ocw.kyushu-u.ac.jp  
    def ScrapKyushuuAcJp(self,UrlCurso,tabla):
        estructuraContenido=['sectionLinks > ul > li > div > a','#course_main_video','#course_main']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #info.kyoto-seika.ac.jp  
    def ScrapKyotoseikaAcJp(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Pagina informativa'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Pagina informativa',tabla)
    #ocw.kaplan.edu  
    def ScrapKaplanEdu(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)

    #ocw.utpl.edu.ec 
    def ScrapUtplEduEc(self,UrlCurso,tabla):
        estructuraContenido=['#portlet-simple-nav > dd.portletItem > a','#parent-fieldname-text','#content']
        self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
    #ocw.sbu.ac.ir   
    def ScrapSbuAcIr(self,UrlCurso,tabla):
        estructuraContenido=['#dnn_ContentPane','#dnn_ContentPane']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #www.kara-s.jp   
    def ScrapKarasJp(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Pagina informativa'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Pagina informativa',tabla)
    #www.kyotomm.jp  
    def ScrapKyotommJp(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Pagina informativa'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Pagina informativa',tabla)
    #learn.uci.edu   
    def ScrapLearnUciEdu(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)

    #media.learn.uci.edu 
    def ScrapMediaLearnUciEdu(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)

    #ocw.usu.ac.id   
    def ScrapUsuAcId(self,UrlCurso,tabla):
        estructuraContenido=['#dg-content-body','#dg-content-body']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #wiki.metropolia.fi  
    def ScrapMetropoliaFi(self,UrlCurso,tabla):
        estructuraContenido=['#main-content','#main-content']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #www.kyoto-seika.ac.jp   
    def ScrapKyotoseikaAcJp(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Pagina informativa'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Pagina informativa',tabla)
    #admission.kyoto-seika.ac.jp 
    def ScrapAdmissionKyotoseikaAcJp(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Pagina informativa'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Pagina informativa',tabla)
    #johokan.kyoto-seika.ac.jp   
    def ScrapJohokanKyotoseikaAcJp(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Pagina informativa'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Pagina informativa',tabla)
    #labspace.open.ac.uk 
    def ScrapOpenAcUk(self,UrlCurso,tabla):
        estructuraContenido=['#middle-column','#middle-column']
        self.ScrapPaginasSinMenu(UrlCurso,tabla,estructuraContenido)
    #opencourse.ndhu.edu.tw  
    def ScrapNdhuEduTw(self,UrlCurso,tabla):
        #estructuraContenido=[' > a','','']
        #self.ScrapPaginasConMenu(UrlCurso,tabla,estructuraContenido)
        print 'Error al Scrapear'
        ObjBd.insertar_datos_trip(UrlCurso,'error','Error al Scrapear',tabla)
    def ScrapUniverdidades(self,linkOcw,tabla):
        Univeridad=linkOcw
        try:
            Univeridad= linkOcw.split('/')[2]
        except Exception, e:
            print 'Url Incorrecta %s'%linkOcw

        if Univeridad == 'www.upv.es':
            self.ScrapUpvEs(linkOcw,tabla)
        elif Univeridad == 'www.unsavirtual.edu.pe:8090':
            self.ScrapUnsavirtualEduPe8090(linkOcw,tabla)
        elif Univeridad == 'www.unav.es':
            self.ScrapUanvEs(linkOcw,tabla)
        elif Univeridad == 'www.uhu.es':
            self.ScrapUhuEs(linkOcw,tabla)
        elif Univeridad == 'www.ocw.unc.edu.ar':
            self.ScrapUncEduAr(linkOcw,tabla)
        elif Univeridad == 'www.lapetus.uchile.cl':
            self.ScrapUchileCl(linkOcw,tabla)
        elif Univeridad == 'www.icesi.edu.co':
            self.ScrapIcesiEduCo(linkOcw,tabla)
        elif Univeridad == 'ocwus.us.es':
            self.ScrapUsEs(linkOcw,tabla)
        elif Univeridad == 'ocwbeta.uji.es':
            self.ScrapUjiEs(linkOcw,tabla)
        elif Univeridad == 'ocw.virtualum.edu.co':
            self.ScrapVirtualumEduCo(linkOcw,tabla)
        elif Univeridad == 'ocw.uv.es':
            self.ScrapUvEs(linkOcw,tabla)
        elif Univeridad == 'ocw.usc.es':
            self.ScrapUscEs(linkOcw,tabla)
        elif Univeridad == 'ocw.usal.es':
            self.ScrapUsalEs(linkOcw,tabla)
        elif Univeridad == 'ocw.upm.es':
            self.ScrapUpmEs(linkOcw,tabla)
        elif Univeridad == 'ocw.upc.edu':
            self.ScrapUpcEdu(linkOcw,tabla)
        elif Univeridad == 'ocw.uoc.edu':
            self.ScrapUocEdu(linkOcw,tabla)
        elif Univeridad == 'ocw.unizar.es':
            self.ScrapUnizarEs(linkOcw,tabla)
        elif Univeridad == 'ocw.univalle.edu.co':
            self.ScrapUnivalleEduCo(linkOcw,tabla)
        elif Univeridad == 'ocw.uniovi.es':
            self.ScrapUnioviEs(linkOcw,tabla)
        elif Univeridad == 'ocw.unican.es':
            self.ScrapUnicanEs(linkOcw,tabla)
        elif Univeridad == 'ocw.unia.es':
            self.ScrapUniaEs(linkOcw,tabla)
        elif Univeridad == 'ocw.uni.edu.pe':
            self.ScrapUniEduPe(linkOcw,tabla)
        elif Univeridad == 'ocw.umh.es':
            self.ScrapUmhEs(linkOcw,tabla)
        elif Univeridad == 'ocw.uma.es':
            self.ScrapUmaEs(linkOcw,tabla)
        elif Univeridad == 'ocw.um.es':
            self.ScrapUmEs(linkOcw,tabla)
        elif Univeridad == 'ocw.ull.es':
            self.ScrapUllEs(linkOcw,tabla)
        elif Univeridad == 'ocw.uis.edu.co':
            self.ScrapUisEduCo(linkOcw,tabla)
        elif Univeridad == 'ocw.uib.es':
            self.ScrapUibEs(linkOcw,tabla)
        elif Univeridad == 'ocw.ugr.es':
            self.ScrapUgrEs(linkOcw,tabla)
        elif Univeridad == 'ocw.udl.cat':
            self.ScrapUdlCat(linkOcw,tabla)
        elif Univeridad == 'ocw.udem.edu.mx':
            self.ScrapUdemEduMx(linkOcw,tabla)
        elif Univeridad == 'ocw.uca.es':
            self.ScrapUcaEs(linkOcw,tabla)
        elif Univeridad == 'ocw.uc3m.es':
            self.ScrapUc3mEs(linkOcw,tabla)
        elif Univeridad == 'ocw.uam.es':
            self.ScrapUamEs(linkOcw,tabla)
        elif Univeridad == 'ocw.ua.es':
            self.ScrapUaEs(linkOcw,tabla)
        elif Univeridad == 'ocw.pucv.cl':
            self.ScrapPucvCl(linkOcw,tabla)
        elif Univeridad == 'ocw.itesm.mx':
            self.ScrapItesmMx(linkOcw,tabla)
        elif Univeridad == 'ocw.innova.uned.es':
            self.ScrapInnovaUnedEs(linkOcw,tabla)
        elif Univeridad == 'ocw.ie.edu':
            self.ScrapInnovaUnedEs(linkOcw,tabla)
        elif Univeridad == 'ocw.flacso.edu.mx:8080':
            self.ScrapFlacsoEduMx8080(linkOcw,tabla)
        elif Univeridad == 'ocw.ehu.es':
            self.ScrapEhuEs(linkOcw,tabla)
        elif Univeridad == 'ocw.ceu.es':
            self.ScrapCeuEs(linkOcw,tabla)
        elif Univeridad == 'ocw.camins.upc.edu':
            self.ScrapCaminsUpcEdu(linkOcw,tabla)
        elif Univeridad == 'ocw.bib.upct.es':
            self.ScrapBibUpctEs(linkOcw,tabla)


        elif Univeridad == 'ocw.mit.edu':
            self.ScrapMitEdu
        elif Univeridad == 'openlearn.open.ac.uk':
            self.ScrapOpenAcUk(linkOcw,tabla)
        elif Univeridad == 'ocw.uci.edu':
            self.ScrapUCiEdu(linkOcw,tabla)
        elif Univeridad == 'opencontent.uct.ac.za':
            self.ScrapUctAcZa(linkOcw,tabla)
        elif Univeridad == 'unow.nottingham.ac.uk':
            self.ScrapNottinghamAcUk(linkOcw,tabla)
        elif Univeridad == 'oer.avu.org':
            self.ScrapAvuOrg(linkOcw,tabla)
        elif Univeridad == 'ocw.hokudai.ac.jp':
            self.ScraphokudaiAcJp(linkOcw,tabla)
        elif Univeridad == 'open.umich.edu':
            self.ScrapUmichEdu(linkOcw,tabla)
        elif Univeridad == 'ocw.metu.edu.tr': 
            self.ScrapMetuEduTr(linkOcw,tabla)
        elif Univeridad == 'ocw.jhsph.edu':
            self.ScrapJhsphEdu(linkOcw,tabla)
        elif Univeridad == 'ocw.korea.edu':
            self.ScrapKoreaEdu(linkOcw,tabla)
        elif Univeridad == 'ocw.tsukuba.ac.jp':
            self.ScrapTsukubaAcJp(linkOcw,tabla)
        elif Univeridad == 'open.agh.edu.pl':
            self.ScrapaghEduPl(linkOcw,tabla)
        elif Univeridad == 'yct.ncku.edu.tw':
            self.ScrapNckuEduTw(linkOcw,tabla)
        elif Univeridad == 'ocw.nd.edu':
            self.ScrapNdEdu(linkOcw,tabla)
        elif Univeridad == 'ocw.tufts.edu':
            self.ScrapTuftsEdu(linkOcw,tabla)
        elif Univeridad == 'ocw.utm.my':
            self.ScrapUtmMy(linkOcw,tabla)
        elif Univeridad == 'ocw.umb.edu':
            self.ScrapUmbEdu(linkOcw,tabla)
        elif Univeridad == 'www5.fgv.br':
            self.ScrapFgvBr(linkOcw,tabla)
        elif Univeridad == 'peer-news.blogspot.com':
            self.ScrapPeernewsBlogspotCom(linkOcw,tabla)
        elif Univeridad == 'feedproxy.google.com': 
            self.ScrapGoogleCom(linkOcw,tabla)
        elif Univeridad == 'ocw.nctu.edu.tw':
            self.ScrapNctuEduTw(linkOcw,tabla)
        elif Univeridad == 'www.open-marhi.ru':
            self.ScrapOpenmarhiRu(linkOcw,tabla)
        elif Univeridad == 'graduateschool.paristech.fr':
            self.ScrapParistechFr(linkOcw,tabla)
        elif Univeridad == 'ocw.tmu.edu.tw:8080':
            self.ScrapTmuEduTw8080(linkOcw,tabla)
        elif Univeridad == 'www.unav.es':
            self.ScrapUnavEs(linkOcw,tabla)
        elif Univeridad == 'ocw.njit.edu': 
            self.ScrapNjitEdu(linkOcw,tabla)
        elif Univeridad == 'ocw.tudelft.nl':
            self.ScrapTudelftNl(linkOcw,tabla)
        elif Univeridad == 'ocw.unu.edu':
            self.ScrapUnuEdu(linkOcw,tabla)
        elif Univeridad == 'www.ocw.titech.ac.jp':
            self.ScrapTitechAcJp(linkOcw,tabla)
        elif Univeridad == 'ocw.uab.cat':
            self.ScrapUabCat(linkOcw,tabla)
        elif Univeridad == 'ocw.uned.ac.cr':
            self.ScrapUnedAcCr(linkOcw,tabla)
        elif Univeridad == 'ocw.itesm.mx':
            self.ScrapItesmMx(linkOcw,tabla)
        elif Univeridad == 'ocw.ie.edu':
            self.ScrapIeEdu(linkOcw,tabla)
        elif Univeridad == 'ocw.kyushu-u.ac.jp':
            self.ScrapKyushuuAcJp(linkOcw,tabla)
        elif Univeridad == 'info.kyoto-seika.ac.jp':
            self.ScrapKyotoseikaAcJp(linkOcw,tabla)
        elif Univeridad == 'ocw.kaplan.edu':
            self.ScrapKaplanEdu(linkOcw,tabla)
        elif Univeridad == 'ocw.utpl.edu.ec' :
            self.ScrapUtplEduEc(linkOcw,tabla)
        elif Univeridad == 'ocw.sbu.ac.ir':
            self.ScrapSbuAcIr(linkOcw,tabla)
        elif Univeridad == 'www.kara-s.jp':
            self.ScrapKarasJp(linkOcw,tabla)
        elif Univeridad == 'www.kyotomm.jp' : 
            self.ScrapKyotommJp(linkOcw,tabla)
        elif Univeridad == 'learn.uci.edu' :
            self.ScrapLearnUciEdu(linkOcw,tabla)
        elif Univeridad == 'media.learn.uci.edu':
            self.ScrapMediaLearnUciEdu(linkOcw,tabla)
        elif Univeridad == 'ocw.usu.ac.id':
            self.ScrapUsuAcId(linkOcw,tabla)
        elif Univeridad == 'wiki.metropolia.fi':
            self.ScrapMetropoliaFi(linkOcw,tabla)
        elif Univeridad == 'www.kyoto-seika.ac.jp':
            self.ScrapKyotoseikaAcJp(linkOcw,tabla)
        elif Univeridad == 'admission.kyoto-seika.ac.jp':
            self.ScrapAdmissionKyotoseikaAcJp(linkOcw,tabla)
        elif Univeridad == 'johokan.kyoto-seika.ac.jp':
            self.ScrapJohokanKyotoseikaAcJp(linkOcw,tabla)
        elif Univeridad == 'labspace.open.ac.uk':
            self.ScrapOpenAcUk(linkOcw,tabla)
        elif Univeridad == 'opencourse.ndhu.edu.tw':
            self.ScrapNdhuEduTw(linkOcw,tabla)
        else:
            print 'no existe universidad %s'%Univeridad
