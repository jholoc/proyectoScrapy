# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 20:18:24 2013

@author: scecy
"""

import nltk
from ClaseExtraccionProcesamientoOersV01 import *
from ClaseExtraerEntidades import *
from nltk.corpus import wordnet

ObjMet = Extraccion_Procesamiento()
#ObjEnti = Extraer_Entidades()
archivo_pdf = PdfFileReader(file("/home/scecy/Oers/Pdfs/01-ushouse-future-of-the-web.pdf", "rb"))
textoextraido = archivo_pdf.getPage(4).extractText()

texto_normalizado=ObjMet.NormalizaTexto(textoextraido)
texto_parrafos = nltk.sent_tokenize(texto_normalizado)
tokens = nltk.word_tokenize(texto_normalizado)
#frec_tokens = ObjMet.FrecuenciaItems(tokens)
tokens_representativos=ObjMet.TokensRepresentativos(tokens)
#idioma = ObjMet.DetectarIdioma(tokens)
#paginas = ObjMet.PdfsMetadatosPaginas("01-ushouse-future-of-the-web.pdf")

#entidades = ObjEnti.ObtenerEntidades(texto_normalizado)
#entidades = ObjEnti.ObtenerEntidades(textoextraido)


lista_palabras=[]
lista_sigwn=[]
valor_retorno=[]
token={}

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
        if char.isalpha() or char.isdigit() or char.ispunctuation() or char.isprintable():
            return False
    return True


def EsStopword(string): #identifica si es un stopwords
    if string.lower() in nltk.corpus.stopwords.words('english'):
        return True
    else:
        return False


def EsPuntuacion(string): #identifica si es un signo, o digito de puntuacion
    for char in string:
        if char.isalpha() or char.isdigit() or char.ispunctuation() or char.isprintable():
            return False
    return True


def EsStopword(string): #identifica si es un stopwords
    if string.lower() in nltk.corpus.stopwords.words('english'):
        return True
    else:
        return False

def BuscarDefiniciones(texto):
    try:
#        wnl = nltk.WordNetLemmatizer()
        for parrafo in texto:  # utiliza cada parrafo de un texto
            oraciones_parrafo = nltk.sent_tokenize(parrafo) #tokeniza el parrafo en oraciones
#            print "---------------------------------------------------"
#            print "TOKENIZACION EN PARRAFOS DEL TEXTO EXTRAIDO"
#            print oraciones_parrafo
            for oracion in oraciones_parrafo: #recorre las oraciones de un parrafo
                sentence = []
                tokens = nltk.word_tokenize(oracion) #tokeniza la oracion
#                print "---------------------------------------------------"
#                print "TOKENIZACION EN ORACIONES DEL PARRAFO"
#                print tokens
                tag_tuples = nltk.pos_tag(tokens) #agrega tag a cada token de la oracion
                for (string, tag) in tag_tuples:
                    token = string,tag #utiliza un arreglo con el token, tag: facilita el proceso de desambiguacion
                    sentence.append(token) #agrega a un arreglo el token con sus valores
            SeleccionSignificado (sentence, oracion, token) #llama al metodo envia los parametros correspondientes, de cada oracion en un parrafo
    except Exception, e:
        print e

def SeleccionSignificado(sentence,oracion,token):
    try:
        for token in sentence: #toma cada token de una oracion
            word = token[0]
            wn_pos = WordnetPosCode(token[1]) #agrega el tag a cada token
            if EsPuntuacion(word): #identifica si es un token de puntuacion
                pass
            elif EsStopword(word): #si encuentra un stopword no lo toma en cuenta
                pass
            elif len(wordnet.synsets(word, wn_pos)) > 0: #verifica que la palabra tenga almenos un significado
                if word in tokens_representativos:
                    valor_retorno=DesambiguarSentidoPalabra(word,wn_pos, oracion, token) #llama al metodo de desambiguacion envia: palabra,tag,oracion
#                    significadoswn=SynsetsWordNet(word,wn_pos, oracion, token)
                    if len(valor_retorno)>3: #verifica que el valor de retorno del metodo de desambiguacion tenga 4 elementos (palabra,tag,definicion, synset)
                        if valor_retorno not in lista_palabras: #verifica que el valor de retorno, para no guardar repeticiones
                            lista_palabras.append(valor_retorno)
#                        if significadoswn not in lista_sigwn:
#                            lista_sigwn.append(significadoswn)
                pass
#        return (lista_palabras)
        lista_palabras
    except Exception, e:
        print e


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

def SynsetsWordNet(word, wn_pos, sentence, token): #desambigua el siginificado de la palabra segun el contexto
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
        return best_sense
    except Exception, e:
        print e





BuscarDefiniciones(texto_parrafos)
print "---------------------------------------------------"
print "TEXTO ORIGINAL"
print textoextraido
#print "---------------------------------------------------"
#print "TEXTO NORMALIZADO"
#print texto_normalizado
#print "---------------------------------------------------"
#print "TOKENS"
#print tokens
#print "---------------------------------------------------"
#print "TAGS"
#print nltk.pos_tag(tokens)
#print "---------------------------------------------------"
#print "FRECUENCIA TOKENS"
#print frec_tokens
#print "---------------------------------------------------"
#print "PALABRAS REPRESENTATIVAS"
#print tokens_representativos
print "---------------------------------------------------"
print "LISTA DE PALABRAS AMBIGUAS Y SU SIGNIFICADO FINAL"
print lista_palabras
print "---------------------------------------------------"
#print "SIGNIFICADOS WORDNET"
#print lista_sigwn
#for l in lista_sigwn:
#    print l
#    definicion=str(l)
#    definiwordnet=definicion[8:len(definicion)-2]
#    palabra=definiwordnet.split('.')[0]
#    tipo=definiwordnet.split('.')[1]
#    print tipo
#    numero=definiwordnet.split('.')[2]
#    print numero
#
#print "---------------------------------------------------"
#print "ENTIDADES"
#print entidades
#print "---------------------------------------------------"
#print "IDIOMA"
#print idioma
#print "---------------------------------------------------"
#print "NUMERO DE PAGINAS"
#print paginas
#print "----------------------ESTADISTICAS-----------------------------"
#print "Texto original, numero de palabras:",len(texto_normalizado)
#print "Palabras representativas, total:",len(tokens_representativos)
#print "Lista de palabras ambiguas, total:",len(lista_palabras)

