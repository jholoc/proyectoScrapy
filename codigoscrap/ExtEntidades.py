#!/usr/bin/env python
#-*-coding: utf-8 *
import nltk
from nltk import RegexpParser,sent_tokenize, word_tokenize, pos_tag, ne_chunk
import goslate
from bd import *
from tokenizarTexto import *

class ExtraerEntidades:
	def recuperarEntidadesEs(self,texto):
		chunker = RegexpParser("""
		ENTI:
		    {<NNP|NNPS>+<NNP|NNPS|NN|NNS>} 
		    {<NN|NNS>+<NN|NNS><JJ>} 
		    {<NNP|NNPS><IN|DT><NNP|NNPS|NN|NNS>}
		    {<NN|NNS><JJ>|<JJ><NN|NNS>}
		    {<NNP|NNPS>}
		ENTIDACOMP:
			{<NN|NNS><ENTI>}
			{<NN|NNS><IN><ENTI>}
			{<ENTI>(<IN>|<IN><DT>)<ENTI|NN|NNS>}
			{<ENTI|ENTIDACOMP><JJ><IN><ENTI|ENTIDACOMP>}
		    {<ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP>}
		    {<ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP>}
		ENTIDACOMP2:
			{<ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP>}
		FECHA:
			{<LS|CD><IN><ENTI><DT><LS|CD>}
			{<LS|CD><IN><ENTI>}
			{<ENTI><DT><LS|CD>}
			{<ENTI><LS|CD>}
		""")
		'''chunker = RegexpParser("""
		ENTI:
		    {<NNP|NNPS>+<NNP|NNPS|NN|NNS>} 
		    {<NN|NNS>+<NN|NNS><JJ>} 
		    {<NNP|NNPS><IN|DT><NNP|NNPS|NN|NNS>}
		    {<NN|NNS><JJ>|<JJ><NN|NNS>}
		    {<NNP|NNPS>}
		ENTIDACOMP:
			{<DT><NN|NNS><ENTI>}
			{<DT><NN|NNS><IN><ENTI>}
			{<ENTI>(<IN>|<IN><DT>)<ENTI|NN|NNS>}
			{<ENTI|ENTIDACOMP><JJ><IN><ENTI|ENTIDACOMP>}
		    {<ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP>}
		    {<ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP>}
		ENTIDACOMP2:
			{<ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP>}
		FECHA:
			{<LS|CD><IN><ENTI><DT><LS|CD>}
			{<LS|CD><IN><ENTI>}
			{<ENTI><DT><LS|CD>}
			{<ENTI><LS|CD>}
		""")'''
		ObjTag = Tokenizar()
		Lista = []
		Lista2 = []
		for sentence in sent_tokenize(texto):
			tags=ObjTag.tagear(sentence)

			tagsentX=word_tokenize(sentence)
			filtered_words = ' '.join(w for w in tagsentX if not w in nltk.corpus.stopwords.words('spanish'))
			parsed = chunker.parse(tags)
			for chunk in parsed:
				if hasattr(chunk, 'node'):
					Lista2.append([chunk.leaves(),filtered_words])
					Lista.append (' '.join(c[0] for c in chunk.leaves()))
		return Lista2

	def recuperarEntidadesEn(self,texto):
		ObjTag = Tokenizar()
		Lista = []
		Lista2= []
		for sentence in sent_tokenize(texto):
			tags=ObjTag.tagear(sentence)
			tagsentX=word_tokenize(sentence)
			filtered_words = ' '.join(w for w in tagsentX if not w in nltk.corpus.stopwords.words('english'))
			parsed = ne_chunk(tags)
			for chunk in parsed:
				if hasattr(chunk, 'node'):
					Lista2.append([chunk.leaves(),filtered_words])
					Lista.append (' '.join(c[0] for c in chunk.leaves()))
		return Lista2

	def recuperarEntidadesToken(self,tokens):
		Lista = []
		Lista2 = []
		sentence= ' '.join(n[0] for n in tokens)
		parsed = ne_chunk(tokens)
		for chunk in parsed:
			if hasattr(chunk, 'node'):
				Lista2.append([chunk.leaves(),sentence])
				Lista.append (' '.join(c[0] for c in chunk.leaves()))
		return Lista2

	def ExtEntidades(self,Entrada):
		if type(Entrada) is str:
			gs= goslate.Goslate()
			idioma=gs.detect(Entrada)
			lenguajes={"auto":"Detect language","af":"Afrikaans","sq":"Albanian","ar":"Arabic","hy":"Armenian","az":"Azerbaijani","eu":"Basque","be":"Belarusian","bn":"Bengali","bs":"Bosnian","bg":"Bulgarian","ca":"Catalan","ceb":"Cebuano","zh-CN":"Chinese","hr":"Croatian","cs":"Czech","da":"Danish","nl":"Dutch","en":"English","eo":"Esperanto","et":"Estonian","tl":"Filipino","fi":"Finnish","fr":"French","gl":"Galician","ka":"Georgian","de":"German","el":"Greek","gu":"Gujarati","ht":"Haitian Creole","ha":"Hausa","iw":"Hebrew","hi":"Hindi","hmn":"Hmong","hu":"Hungarian","is":"Icelandic","ig":"Igbo","id":"Indonesian","ga":"Irish","it":"Italian","ja":"Japanese","jw":"Javanese","kn":"Kannada","km":"Khmer","ko":"Korean","lo":"Lao","la":"Latin","lv":"Latvian","lt":"Lithuanian","mk":"Macedonian","ms":"Malay","mt":"Maltese","mi":"Maori","mr":"Marathi","mn":"Mongolian","ne":"Nepali","no":"Norwegian","fa":"Persian","pl":"Polish","pt":"Portuguese","pa":"Punjabi","ro":"Romanian","ru":"Russian","sr":"Serbian","sk":"Slovak","sl":"Slovenian","so":"Somali","es":"Spanish","sw":"Swahili","sv":"Swedish","ta":"Tamil","te":"Telugu","th":"Thai","tr":"Turkish","uk":"Ukrainian","ur":"Urdu","vi":"Vietnamese","cy":"Welsh","yi":"Yiddish","yo":"Yoruba","zu":"Zulu","af":"Afrikaans","sq":"Albanian","ar":"Arabic","hy":"Armenian","az":"Azerbaijani","eu":"Basque","be":"Belarusian","bn":"Bengali","bs":"Bosnian","bg":"Bulgarian","ca":"Catalan","ceb":"Cebuano","zh-CN":"Chinese (Simplified)","zh-TW":"Chinese (Traditional)","hr":"Croatian","cs":"Czech","da":"Danish","nl":"Dutch","en":"English","eo":"Esperanto","et":"Estonian","tl":"Filipino","fi":"Finnish","fr":"French","gl":"Galician","ka":"Georgian","de":"German","el":"Greek","gu":"Gujarati","ht":"Haitian Creole","ha":"Hausa","iw":"Hebrew","hi":"Hindi","hmn":"Hmong","hu":"Hungarian","is":"Icelandic","ig":"Igbo","id":"Indonesian","ga":"Irish","it":"Italian","ja":"Japanese","jw":"Javanese","kn":"Kannada","km":"Khmer","ko":"Korean","lo":"Lao","la":"Latin","lv":"Latvian","lt":"Lithuanian","mk":"Macedonian","ms":"Malay","mt":"Maltese","mi":"Maori","mr":"Marathi","mn":"Mongolian","ne":"Nepali","no":"Norwegian","fa":"Persian","pl":"Polish","pt":"Portuguese","pa":"Punjabi","ro":"Romanian","ru":"Russian","sr":"Serbian","sk":"Slovak","sl":"Slovenian","so":"Somali","es":"Spanish","sw":"Swahili","sv":"Swedish","ta":"Tamil","te":"Telugu","th":"Thai","tr":"Turkish","uk":"Ukrainian","ur":"Urdu","vi":"Vietnamese","cy":"Welsh","yi":"Yiddish","yo":"Yoruba","zu":"Zulu"}
			idiomaCompleto=lenguajes[idioma]

			if idioma =='es':
				Lista=self.recuperarEntidadesEs(Entrada)
			elif idioma == 'en':
				Lista=self.recuperarEntidadesEn(Entrada)
			else:
				mensaje='El idioma %s no es soportado'%idiomaCompleto
				print mensaje
				mensaje=gs.translate(mensaje, idioma)
				print mensaje
				Lista=[]
		elif type(Entrada) is list:
			Lista=self.recuperarEntidadesToken(Entrada)
		else:
			mensaje='Tipo de datos no soportados'
			print mensaje
			Lista=[]
		return Lista
