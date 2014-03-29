#!/usr/bin/env python
#-*-coding: utf-8 *
import nltk
from nltk import RegexpParser,sent_tokenize, word_tokenize, pos_tag, ne_chunk
import goslate
from bd import *
from tokenizarTexto import *
from nltk.corpus import wordnet
lista_palabras=[]
tokens_representativos=[]
valor_retorno=[]
def WordnetPosCode(tag): #agrega un tag a cada palabra usando wordnet
    try:
        if tag.startswith('NN'):
            return wordnet.NOUN
        elif tag.startswith('VB'):
            return wordnet.VERB
        elif tag.startswith('JJ'):
            return wordnet.ADJ
        elif tag.startswith('RB'):
            return wordnet.ADV
        else:
            return ''
    except Exception, e:
        print e
def EsPuntuacion(string): #identifica si es un signo, o digito de puntuacion
    for char in string:
        #if char.isalpha() or char.isdigit() or char.ispunctuation() or char.isprintable():
        if char.isalpha() or char.isdigit():
            return False
    return True
def EsStopword(string): #identifica si es un stopwords
    if string.lower() in nltk.corpus.stopwords.words('english'):
        return True
    else:
        return False
def Desambiguar(tokens,oracion):
	tokenstag=tokens
	for token in tokenstag: #toma cada token de una oracion
		word = token[0]
		wn_pos = WordnetPosCode(token[1]) #agrega el tag a cada token
		if EsPuntuacion(word): #identifica si es un token de puntuacion
			pass
		elif EsStopword(word): #si encuentra un stopword no lo toma en cuenta
			pass
		elif len(wordnet.synsets(word, wn_pos)) > 0: #verifica que la palabra tenga almenos un significado
			print word
			#print tokens_representativos
			#if word in tokens_representativos:
			if word in word:
				print '-----'
				valor_retorno=DesambiguarSentidoPalabra(word,wn_pos, oracion, token) #llama al metodo de desambiguacion envia: palabra,tag,oracion
				print valor_retorno
				print '-----'
#                    significadoswn=SynsetsWordNet(word,wn_pos, oracion, token)
				if len(valor_retorno)>3: #verifica que el valor de retorno del metodo de desambiguacion tenga 4 elementos (palabra,tag,definicion, synset)
					if valor_retorno not in lista_palabras: #verifica que el valor de retorno, para no guardar repeticiones
						lista_palabras.append(valor_retorno)
#                        if significadoswn not in lista_sigwn:
#                            lista_sigwn.append(significadoswn)
#        return (lista_palabras)
	lista_palabras
def DesambiguarSentidoPalabra(word, wn_pos, sentence, token): #desambigua el siginificado de la palabra segun el contexto
    try:
#        print "***************PALABRA AMBIGUA DE LA ORACION: ",word," ********************"
        senses = wordnet.synsets(word, wn_pos) #toma todos los significados de la palabra
        #toma el numero que cumplen con esta condicion: recorre todos los siginificados, y de cada significado toma sus palabras para comparar si esa palabra se encuentra en la oracion de analisis.
#        print "*****SIGNIFICADOS: ",senses,"*****"
        cfd = nltk.ConditionalFreqDist((sense, def_word) for sense in senses for def_word in sense.definition.split() if def_word in sentence)
        best_sense = senses[0] # start with first sense
        for sense in senses:
            if cfd[sense].N > cfd[best_sense].N: #toma el mejor significado, verificando el significado que tenga mayor frecuencia dentro de una oracion
                best_sense = sense
                token=word,wn_pos,str(best_sense.definition),best_sense #
#                print token
#                print best_sense," ", best_sense.definition
#        print "*********DESAMBIGUACION*********"
#        print token
        return token
    except Exception, e:
        print e
texto=' Fuji of Japón, volcano in south central Honshu that is the highest peak in Japan'
ObjTag = Tokenizar()
l=[('Fuji', 'NNP')]
Desambiguar(l, ' Fuji of Japón')
'''
for sentence in sent_tokenize(texto):
    tags=ObjTag.tagear(sentence)
    print tags    
    tokens_representativos=tags
    Desambiguar(tags, sentence)
print lista_palabras
'''
"""honeySynsets = wordnet.synsets("honey", pos="n")
for synset in honeySynsets:
	print synset.name, synset.definition"""
