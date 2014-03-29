#!/usr/bin/env python
#-*-coding: utf-8 *
import nltk
from nltk import RegexpParser,sent_tokenize, word_tokenize, pos_tag, ne_chunk
import goslate
from bd import *
from tokenizarTexto import *
from nltk.corpus import wordnet
from ExtEntidades import *

ObjExt = ExtraerEntidades()

lista_palabras=[]
tokens_representativos=[]


class Desambiguar():
    def WordnetPosCode(self,tag): #agrega un tag a cada palabra usando wordnet
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
    def EsPuntuacion(self,string): #identifica si es un signo, o digito de puntuacion
        for char in string:
            #if char.isalpha() or char.isdigit() or char.ispunctuation() or char.isprintable():
            if char.isalpha() or char.isdigit():
                return False
        return True
    def EsStopword(self,string): #identifica si es un stopwords
        if string.lower() in nltk.corpus.stopwords.words('english'):
            return True
        else:
            return False
    
    def DesambiguarSentidoPalabra(self,word, wn_pos, sentence, token): #desambigua el siginificado de la palabra segun el contexto
        try:
            senses = wordnet.synsets(word, wn_pos) #toma todos los significados de la palabra
            #toma el numero que cumplen con esta condicion: recorre todos los siginificados, y de cada significado toma sus palabras para comparar si esa palabra se encuentra en la oracion de analisis.
            cfd = nltk.ConditionalFreqDist((sense, def_word) for sense in senses for def_word in sense.definition.split() if def_word in sentence)
            best_sense = senses[0] # start with first sense
            for sense in senses:
                if cfd[sense].N > cfd[best_sense].N: #toma el mejor significado, verificando el significado que tenga mayor frecuencia dentro de una oracion
                    best_sense = sense
                    token=word,wn_pos,str(best_sense.definition),best_sense #
            return token
        except Exception, e:
            print e

    def DesambiguarTexto(self,tokens,oracion):
        lista_palabrasDes=()
        tokenstag=[tokens]
        #print tokens
        for token in tokenstag: #toma cada token de una oracion
            word = token[0]
            wn_pos = self.WordnetPosCode(token[1]) #agrega el tag a cada token
            if self.EsPuntuacion(word): #identifica si es un token de puntuacion
                pass
            elif self.EsStopword(word): #si encuentra un stopword no lo toma en cuenta
                pass
            elif len(wordnet.synsets(word, wn_pos)) > 0: #verifica que la palabra tenga almenos un significado
                if word in word:
                    valor_retorno=self.DesambiguarSentidoPalabra(word,wn_pos, oracion, token) #llama al metodo de desambiguacion envia: palabra,tag,oracion
                    if len(valor_retorno)>3: #verifica que el valor de retorno del metodo de desambiguacion tenga 4 elementos (palabra,tag,definicion, synset)
                        lista_palabrasDes=valor_retorno
                        '''
                        if valor_retorno not in lista_palabrasDes: #verifica que el valor de retorno, para no guardar repeticiones
                            lista_palabrasDes.append(valor_retorno)
                        '''
        return lista_palabrasDes    

    def Desambiguar(self,texto):
        Lista=[]
        if type(texto) is str:
            tokens=ObjExt.ExtEntidades(texto)
            for tokensTexto in tokens:
                texto=tokensTexto[1]
                for j in tokensTexto[0]:
                    token = j
                    Lista.append(self.DesambiguarTexto(token,texto))
        elif type(texto) is list:
            for tokensTexto in texto:
                texto=tokensTexto[1]
                for j in tokensTexto[0]:
                    token = j
                    Lista.append((token,self.DesambiguarTexto(token,texto)))
        else:
            mensaje='Tipo de datos no soportados'
            print mensaje
            Lista=[]
        return Lista

    
