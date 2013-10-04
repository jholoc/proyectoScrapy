import requests
from os.path import basename
from urlparse import urlsplit
import mimetypes;
import urllib
import re

def extraerextoer(url):
    url=url.split('.')
    return url[len(url)-1]

def identificarOer(url):
	patron = re.compile("(\.(pdf|mp3|mp4|wmv|zip|tar|gz|htm|xls|xlsx|doc|docx|odt|ppt|pptx|XLS|DOCX|PPTX|jpg)$)") 
	patronYoutube=re.compile("http://www.youtube.com/watch") 
	busquedayt=patronYoutube.search(url)
	if busquedayt!=None:
		return'video Youtube'
	busqueda=patron.search(url)
	try:
		if busqueda==None:			
			urlOpen=urllib.urlopen(url)
			infoUrl=urlOpen.info()['Content-Type']
			if infoUrl=='application/pdf':
				return 'pdf'
			else:
				if infoUrl=='application/zip':
					return 'zip'
				else:
					return '0'
		else:
			return extraerextoer(url)
	except Exception, e:
				return '0'



url1='http://ocw.tsukuba.ac.jp/iv-1-751f72695b667fa4/5fae7a4d5206-3/lecture1'
url2='http://e.elcomercio.pe/100/doc/0/0/3/7/5/375546.doc'
url3='http://www.youtube.com/watch?v=HE8J2gjPbYQ&feature=youtube_gdata'
url4='http://equellatemp.nottingham.ac.uk/uon/items/c6c045f6-286d-6b9f-b96c-36a998632fc3/1/ViewIMS.jsp?viewMethod=download'
extoer=identificarOer(url4)
if extoer!='0':
	print 'SI es oer y su extencion es: %s'%extoer
else:
	print 'NO ES OER'
#d = urllib.urlopen(url)
#print d.info()['Content-Type']

#print url
#url2 = requests.get(url)
#print url2.url
#print url2.headers
#print url2.headers['Content-Type']

#print basename(urlsplit(url)[2])
#print basename(urlsplit(url2.url)[2])

