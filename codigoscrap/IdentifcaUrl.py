import re,string
from urllib import urlopen

from bs4 import BeautifulSoup
from bs4 import Comment
from bs4 import Tag

from bs4 import *

def removersignos(text):
    signos=(',','|',';','+','{','}','[',']','(',')','^','~','#','<','>'.'→')
    for sig in signos:
        text=text.replace(sig,"")
    return text
def bs4extracion(urlparaestraer):
	webpage = urlopen(urlparaestraer).read()
	soup = BeautifulSoup(webpage)
	[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title','a','&nbsp'])]
	return soup.getText()
    
def extraecontenido(url):
	urlscrap=url
	Soup = bs4extracion(urlscrap)
	return Soup
def encuentraUrl(sentencia):
	sentencialist= sentencia.split()
	
	if len(sentencialist)==1 and 'http://' in sentencialist[0]:
		sentencia=str(extraecontenido(sentencialist[0]).encode('utf-8'))
		sentencia=removersignos(sentencia)
		sentencia= re.sub('(  |\t)+','',sentencia)
		sentencia= re.sub('\n+','.\n',sentencia)
		sentencia= re.sub('\xc2.\.\n| \.\n','',sentencia)
		sentencia= re.sub('\.\.','.',sentencia)
		sentencia = sentencia.strip(' \t\n\r\.')
		
		return sentencia
	else:
		return str(sentencia)






texto='http://oer.avu.org/handle/123456789/251'
texto='http://ocw.unican.es/ensenanzas-tecnicas/economia-y-administracion-de-empresas-para/programa'
#texto='noes'
#texto='noes s'
#texto='http://algo'
texto= encuentraUrl(texto)
print texto