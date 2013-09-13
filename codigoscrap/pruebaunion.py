def unionurl(urlpag,urloer):
	if 'http://' in urloer:
		return urloer
	else:
		list1= urlpag.split('/')
		#print list1
		list2= urloer.split('/')
		#print list2

		list1.extend([element for element in list2 if element not in list1])
		#print list1

		union= '/'.join(list1)
		return union
		
def extrernombremenu(urlmenu):
	url=urlmenu.split('/')
	return url[len(url)-1]
def extrerextoer(urlmenu):
	url=urlmenu.split('.')
	return url[len(url)-1]




web='http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-120-compressible-flow-spring-2003/assignments'
web2='http://ocw.uc3m.es'
web3='/courses/aeronautics-and-astronautics/16-120-compressible-flow-spring-2003/assignments/ps7.pdf'
web4='ISIII_06_EVSpdf'
	
#print unionurl(web,web3)
#print extrernombremenu(web)
print extrerextoer(web3)
