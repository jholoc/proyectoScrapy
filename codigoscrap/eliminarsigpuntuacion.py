import re, string

def remove_punctuation ( text ):
    return re.sub('[%s]' % re.escape(string.punctuation), '', text)
def removersignos(text):
	signos=(',','.',';',':','+','{','}','[',']','(',')','^','~','#')
	for sig in signos:
		text=text.replace(sig,"")
	return text
text='El perro, de San Roque, []{}()no tiene;:, rabo; ni nunca ///lo// ha tenido.'
print text
print remove_punctuation(text)
print removersignos(text)