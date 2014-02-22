#!/usr/bin/env python
#-*-coding: utf-8 *
import nltk
from nltk import RegexpParser,sent_tokenize, word_tokenize, pos_tag, ne_chunk
import goslate
from bd import *

def recuperarEntidades(texto):
	chunker = RegexpParser("""
	ENTI:
	    {<NNP|NNPS>+<NNP|NNPS|NN|NNS>}  # Nouns and Adjectives, terminated with Nouns
	    {<NN|NNS>+<NN|NNS><JJ>} 
	    {<NNP|NNPS><IN|DT><NNP|NNPS|NN|NNS>}
	    {(<NN|NNS><JJ>)|<JJ><NN|NNS>}
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
	Lista = []
	for sentence in sent_tokenize(texto):
		#print sentence  
		tags=tagear(sentence)
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
	return Lista

texto=""" was El monte Fuji ya es Patrimonio de la Humanidad. El volcán Fuji, 13 de Enero del 2014 en  esta,  febrero del 2015 icono de Japón, entró este sábado a formar parte del patrimonio mundial o de la humanidad de la Organización de las Naciones Unidas para la Educación, la Ciencia y la Cultura (Unesco). El Comité del Patrimonio Mundial reunido en Phnom Penh alabó esta cumbre de 3.776 metros de altura que "ha sido inspiración de poetas y artistas y ha sido objeto de peregrinación desde hace siglos". Los japoneses consideran sagrado el Fujiyama (monte Fuyi en japonés), el punto más alto del país, y miles viajan todos los veranos allí para subir a la cumbre, porque es la única época del año que el tiempo lo permite. Los expertos de la Unesco también inscribieron en el patrimonio de la humanidad hoy las terrazas de arroz de Honghe Hani, en China, y el Parque Nacional Sehlabathebe, en Lesoto. Las terrazas de arroz de Hongye Hani cubren 16.603 hectáreas en la provincia de Yunnan y presentan desde hace 1.300 años un paisaje espectacular de arrozales que descienden de manera escalonada desde las montañas Ailao hasta la ribera del río Hong. La Unesco incorporó en la lista 6.550 hectáreas del Parque Nacional Sehlabathebe, en Lesoto, como una extensión de la reserva uKhahlamba Drakensberg, en Sudáfrica. El Comité del Patrimonio Mundial comenzó el pasado día 16 una serie de sesiones en Phnom Penh para examinar 32 candidaturas y clausurará las reuniones el próximo día 27 en el marco de los templos de Angkor, joya arquitectónica del imperio Jemer, en el norte de Camboya. El organismo también ha analizado o analizará el estado de conservación de lugares declarados patrimonio de la humanidad en Siria y Mali, afectados por la guerra, así como el Parque de Doñana, en España, y el casco histórico de Valparaíso, en Chile. EFE
"""
Lista=recuperarEntidades(texto)
for c in sorted(Lista):
	print c 
			#entities.extend([chunk for chunk in chunks if hasattr(chunk, 'node')])"""