#!/usr/bin/env python
#-*-coding: utf-8 *
from tokenizarTexto import *
from DesambiguarTokens import *
from ExtEntidades import *
from DesambiguacionEnlace import *
import re,string


from SPARQLWrapper import SPARQLWrapper, JSON

ObjTag = Tokenizar()
ObjExt = ExtraerEntidades()
ObjDesam = Desambiguar()
ObjDesamEnlace= DesamEnlace()

def imprimilista(lista):
	for lis in lista:
		print lis
	print '---------------------------------------'
'''def ConsuDbpedia(entidades,predicado):
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery("""
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	SELECT *
	WHERE { 
	?label %s "%s"@en
	FILTER regex(str(?label), "http://dbpedia.org/resource/", "i")
	}
	"""%(predicado,entidades))
	sparql.setReturnFormat(JSON)
	return sparql.query().convert()
def ConsuDbpedia2(link,predicado):
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery("""
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	SELECT *
	WHERE {
	<%s> %s ?label
	FILTER regex(str(?label), "http://dbpedia.org/ontology/", "i") 
	}
	"""%(link,predicado))
	sparql.setReturnFormat(JSON)
	return sparql.query().convert()
def ConsuDbpedia3(link,predicado):
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery("""
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	SELECT *
	WHERE {
	<%s> %s ?label
	FILTER regex(str(?label), "http://dbpedia.org/resource/", "i")
	}
	"""%(link,predicado))
	sparql.setReturnFormat(JSON)
	return sparql.query().convert()
def ConsuDbpediaExtraLabel(link,predicado):
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery("""
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	SELECT *
	WHERE {
	<%s> %s ?label
	}
	"""%(link,predicado))
	sparql.setReturnFormat(JSON)
	return sparql.query().convert()
def TipoEntidad(tiposent):
	TipoFinal='Sin Tipo'
	tipoMeclado=''
	for result in tiposent:
		Tipo=(result["label"]["value"])
		TipoEx= Tipo.split('/')
		TipoEx=TipoEx[len(TipoEx)-1]
		if tipoMeclado=='':
			tipoMeclado=TipoEx
		else:
			tipoMeclado=tipoMeclado+'-'+TipoEx
		if TipoEx in ['City','Place','PopulatedPlace', 'Settlement']:
			TipoFinal='GEO'
		if TipoEx in ['Agent']:
			TipoFinal='AGT'
		elif TipoEx in ['Organisation']:
			TipoFinal='ORG'
		elif TipoEx in ['Person']:
			TipoFinal='PER'
		#print'       %s - %s'%(Tipo,TipoEx)
	if tipoMeclado!='' and TipoFinal=='Sin Tipo':
		TipoFinal=tipoMeclado
	return TipoFinal
def eliminasignos(text ):
        return re.sub('[%s]' % re.escape(string.punctuation), '', text)
def SelecionaTipo(listaTipos,contexto):
	listafrec=[]
	#print listaTipos
	for link in listaTipos:
		try:
			LabelsExtraidos=ConsuDbpediaExtraLabel(link[0],'rdfs:label')
		except Exception, e:
			print e
			continue
		LabelsExtraidos=LabelsExtraidos["results"]["bindings"]
		labels=(' '.join(eliminasignos(c["label"]["value"]) for c in LabelsExtraidos)).lower().split(' ')
		labelsSinDuplicados=list(set(labels))
		count=0
		for label in labelsSinDuplicados:
			if label in eliminasignos(contexto.lower()).split(' '):
				count=count+1
		#print '%s ---- %s'%(link[0],link[1])
		#print count
		listafrec.append([count,link[0],link[1]])
	ListaOrdenado= sorted(listafrec,key=lambda x:x[0], reverse=True)
	return ListaOrdenado




def Linkear(entidad,contexto):
	linkear=[]
	try:
		results = ConsuDbpedia(entidad,'rdfs:label')
	except Exception, e:
		print e
		return
	for result in results["results"]["bindings"]:
		link=(result["label"]["value"])
		if 'Category' in link:
			continue
		print link
		
		try:
			results2 = ConsuDbpedia2(link,'rdf:type')
		except Exception, e:
			print e
			continue

		#results2 = ConsuDbpedia2(link,'rdf:type')
		results2 = results2["results"]["bindings"]
		if results2 ==[]:
			print 'NADA'
			UrlyTipo=[]
			results3=ConsuDbpedia3(link,'dbpedia-owl:wikiPageDisambiguates')
			results3=results3["results"]["bindings"]
			for result3 in results3:
				link=(result3["label"]["value"])
				if 'Category:' in link:
					continue
				#print '    %s'%link
				try:
					results4 = ConsuDbpedia2(link,'rdf:type')
				except Exception, e:
					print e
					continue
				#results4 = ConsuDbpedia2(link,'rdf:type')
				
				results4 = results4["results"]["bindings"]
				TipoFinal=TipoEntidad(results4)
				#print '    %s'%TipoFinal
				UrlyTipo.append([link,TipoFinal])
			#print UrlyTipo
			linkear=SelecionaTipo(UrlyTipo,contexto)

		else:
			TipoFinal=TipoEntidad(results2)
			linkear=[[1,link,TipoFinal]]
			print '%s'%TipoFinal
	LisDesyEnlase=[entidad,linkear]
		#break
	print'--------------'
	return LisDesyEnlase'''

import json
lista = [1, 2, (3, 4)] # Note that the 3rd element is a tuple (3, 4)
l=json.dumps(lista) # '[1, 2, [3, 4]]'
print lista
print l


#texto='Fuji  entering your own text in this text box to see what knowledge AlchemyAPI can extract from your unstructured data. University Tecnic  of Loja is the university Catolic of Loja'
texto=""" El monte Fuji ya es Patrimonio de la Humanidad. El volcán Fuji, Japón, entró este sábado a formar parte del patrimonio mundial o de la humanidad de la Organización de las Naciones Unidas para la Educación, la Ciencia y la Cultura (Unesco). El Comité del Patrimonio Mundial reunido en Phnom Penh alabó esta cumbre de 3.776 metros de altura que "ha sido inspiración de poetas y artistas y ha sido objeto de peregrinación desde hace siglos". Los japoneses consideran sagrado el Fujiyama (monte Fuyi en japonés), el punto más alto del país, y miles viajan todos los veranos allí para subir a la cumbre, porque es la única época del año que el tiempo lo permite. Los expertos de la Unesco también inscribieron en el patrimonio de la humanidad hoy las terrazas de arroz de Honghe Hani, en China, y el Parque nacional de Sehlabathebe, en Lesoto. Las terrazas de arroz de Hongye Hani cubren 16.603 hectáreas en la provincia de Yunnan y presentan desde hace 1.300 años un paisaje espectacular de arrozales que descienden de manera escalonada desde las montañas Ailao hasta la ribera del río Hong. La Unesco incorporó en la lista 6.550 hectáreas del Parque Nacional Sehlabathebe, en Lesoto, como una extensión de la reserva uKhahlamba Drakensberg, en Sudáfrica. El Comité del Patrimonio Mundial comenzó el pasado día 16 una serie de sesiones en Phnom Penh para examinar 32 candidaturas y clausurará las reuniones el próximo día 27 en el marco de los templos de Angkor, joya arquitectónica del imperio Jemer, en el norte de Camboya. El organismo también ha analizado o analizará el estado de conservación de lugares declarados patrimonio de la humanidad en Siria y Mali, afectados por la guerra, así como el Parque de Doñana, en España, y el casco histórico de Valparaíso, en Chile. EFE """
#texto='''It is currently a work in progress, but the fundamentals are in place and you can already start building kick-ass browsable Web APIs with it. If you want to start using Flask API right now go ahead and do so, but be sure to follow the release notes of new versions carefully.'''
#lista=[('If', 'IN'), ('you', 'PRP'), ('want', 'VBP'), ('to', 'TO'), ('start', 'VB'), ('using', 'VBG'), ('Flask', 'NNP'), ('API', 'NNP'), ('right', 'NN'), ('now', 'RB'), ('go', 'VBP'), ('ahead', 'RB'), ('and', 'CC'), ('do', 'VBP'), ('so', 'RB'), (',', ','), ('but', 'CC'), ('be', 'VB'), ('sure', 'JJ'), ('to', 'TO'), ('follow', 'VB'), ('the', 'DT'), ('release', 'NN'), ('notes', 'NNS'), ('of', 'IN'), ('new', 'JJ'), ('versions', 'NNS'), ('carefully', 'RB'), ('.', '.')]
#lista=[('Jhonny', 'NNP'), ('Zaruma', 'NNP'), ('Try', 'NNP'), ('entering', 'NN'), ('your', 'PRP$'), ('own', 'JJ'), ('text', 'NN'), ('in', 'IN'), ('this', 'DT'), ('text', 'NN'), ('box', 'NN'), ('to', 'TO'), ('see', 'VB'), ('what', 'WP'), ('knowledge', 'NN'), ('AlchemyAPI', 'NNP'), ('can', 'MD'), ('extract', 'VB'), ('from', 'IN'), ('your', 'PRP$'), ('unstructured', 'VBN'), ('data.', 'NNP'), ('University', 'NNP'), ('Tecnic', 'NNP'), ('of', 'IN'), ('Loja', 'NNP'), ('is', 'VBZ'), ('the', 'DT'), ('university', 'NN'), ('Catolic', 'NNP'), ('of', 'IN'), ('Loja', 'NNP')]
#texto="Fuji of Japón Fuji, volcano in south central Honshu Fuji that is the highest peak in Japan Fuji"
#texto='''Bill Gates is the best. AlchemyAPI uses natural language processing, artificial intelligence, deep learning and massive-scale web crawling to power it's text analysis capabilities. Try entering your own text in this text box to see what knowledge AlchemyAPI can extract from your unstructured data.'''
#texto='''Com três principais actividades, a Unidade 2 considera algoritmos computacionais para encontrar plausíveis soluções e óptimas para o problema de programação linear situações do tipo formulada na Unidade 1. Actividade 3 examina as condições óptimas de uma solução, que é realmente de reconhecendo quando alguém está se movendo e chegando a uma candidata e melhor solução. Actividade 4 discute a peça central de métodos algébricos computacionais de ataque, o famoso algoritmo Simplex. Este módulo centra-se na lógica do algoritmo e na útil associação das propriedades qualitativas de dualidade, degeneração, e eficiência. Os toques finais sobre a actividade do problema de estabilidade e obtenção de óptimas soluções em relação às variações de entrada específicas ou factores específicos de saída nas restrições e funções objectivas. Este é assim chamado optimização de análise de sensibilidade e é apresentado aqui apenas ao nível da valorização das estratégias analíticas empregadas.'''
#texto='''Risk Aversion and Invertment Decisions : part II'''
#texto='''he more things change... Yes, I'm inclined to agree, especially with regards to the historical relationship between stock prices and bond yields. The two have generally traded together, rising during periods of economic growth and falling during periods of contraction. Consider the period from 1998 through 2010, during which the U.S. economy experienced two expansions as well as two recessions: Then central banks came to the rescue. Fed Chairman Ben Bernanke led from Washington with the help of the bank's current $3.6T balance sheet. He's accompanied by Mario Draghi at the European Central Bank and an equally forthright Shinzo Abe in Japan. Their coordinated monetary expansion has provided all the sugar needed for an equities moonshot, while they vowed to hold global borrowing costs at record lows.'''
texto='''One year ago, several hours before cities across the United States started their annual fireworks displays, a different type of fireworks were set off at the European Center for Nuclear Research (CERN) in Switzerland. At 9:00 a.m., physicists announced to the world that they had found something they had been searching for for nearly 50 years: the elusive Higgs boson. Today, on the anniversary of its discovery, are we any closer to figuring out what that particle's true identity is? The Higgs boson is popularly referred to as "the God particle," perhaps because of its role in giving other particles their mass. However, it's not the boson itself that gives mass. Back in 1964, Peter Higgs proposed a theory that described a universal field (similar to an electric or a magnetic field) that particles interacted with.'''
#texto='''Jhonny Zaruma, esta en la canton esta en Quito, Ecuador, Peru, Argentina, Israel, Korea, China, North Korea, Loja, Ambato, Zamora, Medellin, Buenos Aires, Paris, Francia, Colombia, Chile, Piura, Distrito Federal, Mexico, Honduras, Montanita'''
texto='''This site uses cookies. By continuing to browse the site you are agreeing to our use of cookies. X Bloomberg.com GLOBAL EDITION Businessweek.com Company About Florida plans to file a U.S. Supreme Court lawsuit against Georgia, saying the state is consuming too much water that would otherwise flow to Florida, the latest battle nationally over an increasingly scarce resource. The dispute is fueled by the rapid growth of the metropolitan area surrounding Atlanta, which is demanding more water and hurting the oyster industry in Northwest Florida, Florida Governor Rick Scott, 60, said yesterday. Scott, a Republican, said he would file suit next month after the two states couldn’t reach an agreement. “That’s our water,” Scott told reporters while standing next to the Apalachicola Bay in the Florida Panhandle. “They’ve impacted our families. They’ve impacted the livelihood of people down here.” For more than 20 years, Florida, Georgia and Alabama have been mired in negotiations over the distribution of water shared by the three states. The dispute is emblematic of an increasingly common challenge facing cities and states across the country: Demand for water is outpacing supply as urban development and population growth sap resources. Urban development in Georgia has led to an increased need for water, much of it pumped from a river basin that’s also relied on by Florida and Alabama. ‘Unchecked Consumption’ Georgia has engaged in “unchecked consumption of water,” while not negotiating in good faith, making a lawsuit the only way to resolve the matter, Scott said in a statement. Georgia Governor Nathan Deal, 70, a Republican, said in a statement that Scott’s planned lawsuit is a “frivolous waste of time and money.” “Scott’s threat to sue my state in the U.S. Supreme Court greatly disappoints me after I negotiated in good faith for two years,” Deal said. “More than a year ago, I offered a framework for a comprehensive agreement. Florida never responded.” Legal disputes between states must be heard by the U.S. Supreme Court, instead of going through lower courts first, according to the Constitution. The U.S. Army Corps of Engineers is responsible for managing the water in the states’ shared river basin, which spans the Apalachicola, Chattahoochee and Flint rivers. Fighting Georgia Officials in Alabama, which has also fought Georgia over water distribution, haven’t said whether they’ll join in the lawsuit. The state will consider “all available options” to protect its water rights, said Jennifer Ardis, a spokeswoman for Alabama Governor Robert Bentley, a Republican, in an e-mail. At a hearing yesterday in Apalachicola, U.S. Senator Bill Nelson, a Florida Democrat, and U.S Senator Marco Rubio, a Florida Republican, both blamed Georgia for taking more than its fair share of water. Georgia’s consumption, along with a drought last year, threatens fisheries and economic development in the Florida Panhandle, they said. The oyster industry in Apalachicola Bay has collapsed over the past year. The National Oceanic and Atmospheric Administration issued a fishery disaster declaration on Aug. 12 over oysters. Scott and Nelson have both pushed for the disaster declaration during the past year. “The changes to water flow have decimated a once booming industry, but I’m hopeful we can soon start to turn things around,” Nelson said in a statement. Apalachicola Bay supplies 10 percent of the nation’s oysters, according to a December report by Florida’s Fish and Wildlife Conservation Commission. The industry supports about 2,500 jobs in Florida, according to the report. Many of those jobs, and perhaps the industry, are at risk due to the lack of fresh water flowing into the bay, Rubio said. “We don’t have time,” said Rubio. “In a couple years, there may not be anybody left to save around here in this industry.” To contact the reporters on this story: Toluse Olorunnipa in Tallahassee, Florida at tolorunnipa@bloomberg.net; Michael C. Bender in Washington at mbender10@bloomberg.net To contact the editor responsible for this story: Stephen Merelman at smerelman@bloomberg.net'''

a='monte Fuji'
print a.capitalize()
a='monte fuji'
print a.capitalize()
print a.title()
import goslate
gs = goslate.Goslate()
b='''El Comité Patrimonio Mundial reunido Phnom Penh alabó cumbre  metros altura sido inspiración poetas artistas sido objeto peregrinación hace siglos  '''
print gs.detect(b)

desorden=[[1,'qsjq','geo'],[1,'qsjsdsdq','geo'],[1,'aqsjq','geo'],[3,'zqsjq','geo'],[2,'zqsjq','per']]
print desorden
print sorted(desorden,key=lambda x:x[0], reverse=True)
print desorden.sort(key=lambda x: x[0])

lista1="Lunes-Martes"
lista1= texto.split('-')
#if 'di'.lower() in [x.lower() for x in lista1]:
#	print 'Si hay 1'
#else:
#	print 'no'
if 'ciudad'.lower() in texto.lower().split(' '):
	print 'Si hay 1'
else:
	print 'no'


#li1= ObjTag.tagear(texto)
#imprimilista(li1)
li2= ObjExt.ExtEntidades(texto)
imprimilista(li2)
li3= ObjDesam.Desambiguar(li2)
#imprimilista(li3)
li4=ObjDesamEnlace.DesamEnlace(li2)
imprimilista(li4)
#print li


