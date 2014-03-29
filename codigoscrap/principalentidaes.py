#!/usr/bin/env python
#-*-coding: utf-8 *
from tokenizarTexto import *
from DesambiguarTokens import *
from ExtEntidades import *
ObjTag = Tokenizar()
ObjExt = ExtraerEntidades()
ObjDesam = Desambiguar()

def imprimilista(lista):
	for lis in lista:
		print lis
	print '---------------------------------------'

#texto='Fuji  entering your own text in this text box to see what knowledge AlchemyAPI can extract from your unstructured data. University Tecnic  of Loja is the university Catolic of Loja'
texto=""" was El monte Fuji ya es Patrimonio de la Humanidad. El volcán Fuji, 13 de Enero del 2014 en  esta,  febrero del 2015 icono de Japón, entró este sábado a formar parte del patrimonio mundial o de la humanidad de la Organización de las Naciones Unidas para la Educación, la Ciencia y la Cultura (Unesco). El Comité del Patrimonio Mundial reunido en Phnom Penh alabó esta cumbre de 3.776 metros de altura que "ha sido inspiración de poetas y artistas y ha sido objeto de peregrinación desde hace siglos". Los japoneses consideran sagrado el Fujiyama (monte Fuyi en japonés), el punto más alto del país, y miles viajan todos los veranos allí para subir a la cumbre, porque es la única época del año que el tiempo lo permite. Los expertos de la Unesco también inscribieron en el patrimonio de la humanidad hoy las terrazas de arroz de Honghe Hani, en China, y el Parque Nacional Sehlabathebe, en Lesoto. Las terrazas de arroz de Hongye Hani cubren 16.603 hectáreas en la provincia de Yunnan y presentan desde hace 1.300 años un paisaje espectacular de arrozales que descienden de manera escalonada desde las montañas Ailao hasta la ribera del río Hong. La Unesco incorporó en la lista 6.550 hectáreas del Parque Nacional Sehlabathebe, en Lesoto, como una extensión de la reserva uKhahlamba Drakensberg, en Sudáfrica. El Comité del Patrimonio Mundial comenzó el pasado día 16 una serie de sesiones en Phnom Penh para examinar 32 candidaturas y clausurará las reuniones el próximo día 27 en el marco de los templos de Angkor, joya arquitectónica del imperio Jemer, en el norte de Camboya. El organismo también ha analizado o analizará el estado de conservación de lugares declarados patrimonio de la humanidad en Siria y Mali, afectados por la guerra, así como el Parque de Doñana, en España, y el casco histórico de Valparaíso, en Chile. EFE """
#texto='''It is currently a work in progress, but the fundamentals are in place and you can already start building kick-ass browsable Web APIs with it. If you want to start using Flask API right now go ahead and do so, but be sure to follow the release notes of new versions carefully.'''
#lista=[('If', 'IN'), ('you', 'PRP'), ('want', 'VBP'), ('to', 'TO'), ('start', 'VB'), ('using', 'VBG'), ('Flask', 'NNP'), ('API', 'NNP'), ('right', 'NN'), ('now', 'RB'), ('go', 'VBP'), ('ahead', 'RB'), ('and', 'CC'), ('do', 'VBP'), ('so', 'RB'), (',', ','), ('but', 'CC'), ('be', 'VB'), ('sure', 'JJ'), ('to', 'TO'), ('follow', 'VB'), ('the', 'DT'), ('release', 'NN'), ('notes', 'NNS'), ('of', 'IN'), ('new', 'JJ'), ('versions', 'NNS'), ('carefully', 'RB'), ('.', '.')]
#lista=[('Jhonny', 'NNP'), ('Zaruma', 'NNP'), ('Try', 'NNP'), ('entering', 'NN'), ('your', 'PRP$'), ('own', 'JJ'), ('text', 'NN'), ('in', 'IN'), ('this', 'DT'), ('text', 'NN'), ('box', 'NN'), ('to', 'TO'), ('see', 'VB'), ('what', 'WP'), ('knowledge', 'NN'), ('AlchemyAPI', 'NNP'), ('can', 'MD'), ('extract', 'VB'), ('from', 'IN'), ('your', 'PRP$'), ('unstructured', 'VBN'), ('data.', 'NNP'), ('University', 'NNP'), ('Tecnic', 'NNP'), ('of', 'IN'), ('Loja', 'NNP'), ('is', 'VBZ'), ('the', 'DT'), ('university', 'NN'), ('Catolic', 'NNP'), ('of', 'IN'), ('Loja', 'NNP')]
#texto="Fuji of Japón Fuji, volcano in south central Honshu Fuji that is the highest peak in Japan Fuji"


#li= ObjExt.ExtEntidades(lista)
li1= ObjExt.ExtEntidades(texto)
li2= ObjTag.tagear(texto)
li3= ObjDesam.Desambiguar(li1)
#print li

imprimilista(li1)
imprimilista(li2)
imprimilista(li3)