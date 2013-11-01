# -*- coding: utf-8 -*-
import requests
#from os.path import basename
#from urlparse import urlsplit
#import mimetypes;
import urllib
import httplib,urlparse # para el metodo 
import re,string,requests

def extraerextoer(url):
    url=url.split('.')
    return url[len(url)-1]

def identificarOer(url):
	if identificarOer2(url)=='0':
		print 'if'
		url=requests.get(url).url
		print 'requests: %s'%url
		return identificarOer2(url)
	else:
		print 'else'
		return identificarOer2(url)

def identificarOer2(url):
	patron = re.compile("(\.(pdf|mp3|mp4|wmv|zip|rar|tar|gz|htm|xls|xlsx|doc|docx|odt|ppt|pptx|XLS|DOCX|PPTX|jpg)$)")
	if "http://www.youtube.com/watch" in url:
		return'video Youtube'
	busqueda=patron.search(url)
	try:
		if busqueda==None:	
			urlOpen=urllib.urlopen(url)
			infoUrl=urlOpen.info()['Content-Type']
			print infoUrl
			#print urlOpen.info()
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
			return extraerextoer(url)
	except Exception, e:
				return '0'
def getFinalUrl(url):
    "Navigates Through redirections to get final url."
    parsed = urlparse.urlparse(url)
    conn = httplib.HTTPConnection(parsed.netloc)
    conn.request("HEAD",parsed.path)
    response = conn.getresponse()
    if str(response.status).startswith("3"):
        new_location = [v for k,v in response.getheaders() if k == "location"][0]
        return getFinalUrl(new_location)
    return url



url1='http://ocw.tsukuba.ac.jp/iv-1-751f72695b667fa4/5fae7a4d5206-3/lecture1'
url2='http://e.elcomercio.pe/100/doc/0/0/3/7/5/375546.doc'
url3='http://www.youtube.com/watch?v=HE8J2gjPbYQ&feature=youtube_gdata'
url4='http://140.116.203.51/tlcenter/fireenergy/pdf_20101025.rar'
url4='http://open.agh.edu.pl/mod/resource/view.php?inpopup=true&id=999'
url4='http://ocw.ugr.es/mod/resource/view.php?id=583'
url4='http://ocw.ugr.es/file.php/20/relacion-aritmetica-entera.pdf?forcedownload=1'
url4='http://ocw.korea.edu/ocw/college-of-engineering/electronic-circuits-i/lecture-notes-1/midterm-project'
print url4
"""url5 = requests.get(url3)
print url5.url
url4=url5.url"""
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

