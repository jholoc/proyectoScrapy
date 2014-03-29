#!/usr/bin/env python
#-*-coding: utf-8 *
import nltk
from nltk import RegexpParser,sent_tokenize, word_tokenize, pos_tag, ne_chunk
import goslate
from bd import *
from tokenizarTexto import *
from DesambiguarTokens import *

class ExtraerEntidades:
	def recuperarEntidadesEs(texto):
		chunker = RegexpParser("""
		ENTI:
		    {<NNP|NNPS>+<NNP|NNPS|NN|NNS>}  # Nouns and Adjectives, terminated with Nouns
		    {<NN|NNS>+<NN|NNS><JJ>} 
		    {<NNP|NNPS><IN|DT><NNP|NNPS|NN|NNS>}
		    {<NN|NNS><JJ>|<JJ><NN|NNS>}
		    {<NNP|NNPS>}
		ENTIDACOMP:
			{<DT><NN|NNS><ENTI>}
			{<DT><NN|NNS><IN><ENTI>}
			{<ENTI>(<IN>|<IN><DT>)<ENTI|NN|NNS>}
			{<ENTI|ENTIDACOMP><JJ><IN><ENTI|ENTIDACOMP>}
		    {<ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP>}  # Above, connected with in/of/etc...
		    {<ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP>}
		ENTIDACOMP2:
			{<ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP>}
		FECHA:
			{<LS|CD><IN><ENTI><DT><LS|CD>}
			{<LS|CD><IN><ENTI>}
			{<ENTI><DT><LS|CD>}
			{<ENTI><LS|CD>}


		""")
		ObjTag = Tokenizar()
		Lista = []
		for sentence in sent_tokenize(texto):
			#print sentence  
			tags=ObjTag.tagear(sentence)
			#tags=tagear(traducir(word_tokenize(sentence)))
			#print tags
			parsed = chunker.parse(tags)
			print parsed
			for chunk in parsed:
				#print chunk
				#if hasattr(chunk, 'node'):
				#	print chunk.node
				if hasattr(chunk, 'node'):
					#	print chunk	
					#print chunk.leaves()
					#print ' '.join(c[0] for c in chunk.leaves())
					Lista.append (' '.join(c[0] for c in chunk.leaves()))
			print Lista
		return Lista
	def recuperarEntidadesEn(texto):
		ObjTag = Tokenizar()
		ObjDes = Desambiguar()
		Lista = []
		Lista2= []
		for sentence in sent_tokenize(texto):
			#print sentence  
			tags=ObjTag.tagear(sentence)
			#tags=tagear(traducir(word_tokenize(sentence)))
			print tags
			parsed = ne_chunk(tags)
			print parsed
			for chunk in parsed:
				#print chunk
				#if hasattr(chunk, 'node'):
				#	print chunk.node
				if hasattr(chunk, 'node'):
					#print chunk	
					#print chunk.leaves()
					Lista2.append(chunk.leaves()[0])
					#print ' '.join(c[0] for c in chunk.leaves())
					Lista.append (' '.join(c[0] for c in chunk.leaves()))
			print Lista2
			print ObjDes.DesambiguarTexto(Lista2, sentence)
			Lista2=[]
		return Lista
	def ExtEntidades(self,texto):
		ObjTag = Tokenizar()
		if type(texto) is str:
			

		elif type(texto) is list:


	texto=""" was El monte Fuji ya es Patrimonio de la Humanidad. El volcán Fuji, 13 de Enero del 2014 en  esta,  febrero del 2015 icono de Japón, entró este sábado a formar parte del patrimonio mundial o de la humanidad de la Organización de las Naciones Unidas para la Educación, la Ciencia y la Cultura (Unesco). El Comité del Patrimonio Mundial reunido en Phnom Penh alabó esta cumbre de 3.776 metros de altura que "ha sido inspiración de poetas y artistas y ha sido objeto de peregrinación desde hace siglos". Los japoneses consideran sagrado el Fujiyama (monte Fuyi en japonés), el punto más alto del país, y miles viajan todos los veranos allí para subir a la cumbre, porque es la única época del año que el tiempo lo permite. Los expertos de la Unesco también inscribieron en el patrimonio de la humanidad hoy las terrazas de arroz de Honghe Hani, en China, y el Parque Nacional Sehlabathebe, en Lesoto. Las terrazas de arroz de Hongye Hani cubren 16.603 hectáreas en la provincia de Yunnan y presentan desde hace 1.300 años un paisaje espectacular de arrozales que descienden de manera escalonada desde las montañas Ailao hasta la ribera del río Hong. La Unesco incorporó en la lista 6.550 hectáreas del Parque Nacional Sehlabathebe, en Lesoto, como una extensión de la reserva uKhahlamba Drakensberg, en Sudáfrica. El Comité del Patrimonio Mundial comenzó el pasado día 16 una serie de sesiones en Phnom Penh para examinar 32 candidaturas y clausurará las reuniones el próximo día 27 en el marco de los templos de Angkor, joya arquitectónica del imperio Jemer, en el norte de Camboya. El organismo también ha analizado o analizará el estado de conservación de lugares declarados patrimonio de la humanidad en Siria y Mali, afectados por la guerra, así como el Parque de Doñana, en España, y el casco histórico de Valparaíso, en Chile. EFE
	"""
	texto='''It is currently a work in progress, but the fundamentals are in place and you can already start building kick-ass browsable Web APIs with it. If you want to start using Flask API right now go ahead and do so, but be sure to follow the release notes of new versions carefully.'''
	#texto='''Il est actuellement un travail en cours, mais les principes fondamentaux sont en place et vous pouvez déjà commencer à construire Kick-Ass API Web consultable avec elle. Si vous voulez commencer à utiliser l'API Flacon maintenant aller de l'avant et le faire, mais assurez-vous de suivre les notes de version de nouvelles versions avec soin.'''
	texto='''В настоящее время это в стадии разработки, но основные принципы находятся на месте и вы уже можете начать строить обалденная доступным для просмотра веб-интерфейсы API с ним. Если вы хотите, чтобы начать использовать Фляга API прямо сейчас идти вперед и делать это так, но обязательно следуйте примечания к выпуску новых версий тщательно.'''
	#texto='''Quito is a city of Ecuador'''
	#texto=''' Fuji is In this unit we start with the study of both the Lebesgue outer measure and the real line before we look at the Lebesgue measurable subsets of the real line. A look at the sigma algebra of subsets of a given underlying set gives rise to measurable space on which we can also study a class of functions called measurable functions. A part from the Lebesgue measure we also study an abstract measure leading to an abstract measure space on which we introduce an abstract integral. Finally a brief comparison of the Lebesgue integral and the well known Riemann integral is also essential in this unit.'''
	texto='''AlchemyAPI uses natural language processing, artificial intelligence, deep learning and massive-scale web crawling to power it's text analysis capabilities. Try entering your own text in this text box to see what knowledge AlchemyAPI can extract from your unstructured data.'''

	gs= goslate.Goslate()
	idioma=gs.detect(texto)
	#print idioma
	lenguajes={"auto":"Detect language","af":"Afrikaans","sq":"Albanian","ar":"Arabic","hy":"Armenian","az":"Azerbaijani","eu":"Basque","be":"Belarusian","bn":"Bengali","bs":"Bosnian","bg":"Bulgarian","ca":"Catalan","ceb":"Cebuano","zh-CN":"Chinese","hr":"Croatian","cs":"Czech","da":"Danish","nl":"Dutch","en":"English","eo":"Esperanto","et":"Estonian","tl":"Filipino","fi":"Finnish","fr":"French","gl":"Galician","ka":"Georgian","de":"German","el":"Greek","gu":"Gujarati","ht":"Haitian Creole","ha":"Hausa","iw":"Hebrew","hi":"Hindi","hmn":"Hmong","hu":"Hungarian","is":"Icelandic","ig":"Igbo","id":"Indonesian","ga":"Irish","it":"Italian","ja":"Japanese","jw":"Javanese","kn":"Kannada","km":"Khmer","ko":"Korean","lo":"Lao","la":"Latin","lv":"Latvian","lt":"Lithuanian","mk":"Macedonian","ms":"Malay","mt":"Maltese","mi":"Maori","mr":"Marathi","mn":"Mongolian","ne":"Nepali","no":"Norwegian","fa":"Persian","pl":"Polish","pt":"Portuguese","pa":"Punjabi","ro":"Romanian","ru":"Russian","sr":"Serbian","sk":"Slovak","sl":"Slovenian","so":"Somali","es":"Spanish","sw":"Swahili","sv":"Swedish","ta":"Tamil","te":"Telugu","th":"Thai","tr":"Turkish","uk":"Ukrainian","ur":"Urdu","vi":"Vietnamese","cy":"Welsh","yi":"Yiddish","yo":"Yoruba","zu":"Zulu","af":"Afrikaans","sq":"Albanian","ar":"Arabic","hy":"Armenian","az":"Azerbaijani","eu":"Basque","be":"Belarusian","bn":"Bengali","bs":"Bosnian","bg":"Bulgarian","ca":"Catalan","ceb":"Cebuano","zh-CN":"Chinese (Simplified)","zh-TW":"Chinese (Traditional)","hr":"Croatian","cs":"Czech","da":"Danish","nl":"Dutch","en":"English","eo":"Esperanto","et":"Estonian","tl":"Filipino","fi":"Finnish","fr":"French","gl":"Galician","ka":"Georgian","de":"German","el":"Greek","gu":"Gujarati","ht":"Haitian Creole","ha":"Hausa","iw":"Hebrew","hi":"Hindi","hmn":"Hmong","hu":"Hungarian","is":"Icelandic","ig":"Igbo","id":"Indonesian","ga":"Irish","it":"Italian","ja":"Japanese","jw":"Javanese","kn":"Kannada","km":"Khmer","ko":"Korean","lo":"Lao","la":"Latin","lv":"Latvian","lt":"Lithuanian","mk":"Macedonian","ms":"Malay","mt":"Maltese","mi":"Maori","mr":"Marathi","mn":"Mongolian","ne":"Nepali","no":"Norwegian","fa":"Persian","pl":"Polish","pt":"Portuguese","pa":"Punjabi","ro":"Romanian","ru":"Russian","sr":"Serbian","sk":"Slovak","sl":"Slovenian","so":"Somali","es":"Spanish","sw":"Swahili","sv":"Swedish","ta":"Tamil","te":"Telugu","th":"Thai","tr":"Turkish","uk":"Ukrainian","ur":"Urdu","vi":"Vietnamese","cy":"Welsh","yi":"Yiddish","yo":"Yoruba","zu":"Zulu"}
	idiomaCompleto=lenguajes[idioma]
	#print idiomaCompleto


	if idioma =='es':
		Lista=recuperarEntidadesEs(texto)
	elif idioma == 'en':
		Lista=recuperarEntidadesEn(texto)
	else:
		mensaje='El idioma %s no es soportado'%idiomaCompleto
		print mensaje
		mensaje=gs.translate(mensaje, idioma)
		print mensaje
		Lista=[]
	for c in sorted(Lista):
		print c 
				#entities.extend([chunk for chunk in chunks if hasattr(chunk, 'node')])"""