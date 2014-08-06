#!/usr/bin/env python
#-*-coding: utf-8 *
import re,string
from tokenizarTexto import *
from ExtEntidades import *
from SPARQLWrapper import SPARQLWrapper, JSON
import unicodedata

import goslate
gs = goslate.Goslate()

ObjTag = Tokenizar()
ObjExt = ExtraerEntidades()


class DesamEnlace():

	def ConsuDbpediaa(self,entidades,predicado,idioma):
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sentencia="""
		SELECT *
		WHERE { ?label %s ?term .
		FILTER (lcase(str(?term)) = "%s") .
		FILTER (lang(?term)="%s")  .
		FILTER regex(str(?label), "http://dbpedia.org/resource/", "i")
		}
		"""%(predicado,entidades.lower(),idioma)
		sentencia="""
		SELECT *
		WHERE { ?label %s ?term .
		FILTER (lcase(str(?term)) = "%s") .
		FILTER regex(str(?label), "http://dbpedia.org/resource/", "i")
		}
		"""%(predicado,entidades.lower())
		print sentencia
		sparql.setQuery(sentencia)
		sparql.setReturnFormat(JSON)
		print entidades
		print sparql.query().convert()
		return sparql.query().convert()
	def ConsuDbpedia(self,entidades,predicado,idioma):
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setQuery("""
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		SELECT *
		WHERE { 
		?label %s "%s"@%s
		FILTER regex(str(?label), "http://dbpedia.org/resource/", "i")
		}
		"""%(predicado,entidades,idioma))
		sparql.setReturnFormat(JSON)
		return sparql.query().convert()
	def ConsuDbpedia2(self,link,predicado):
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
	def ConsuDbpedia3(self,link,predicado):
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setQuery("""
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX rdf: <http://www.w3.org/1999/02/20002-rdf-syntax-ns#>
		SELECT *
		WHERE {
		<%s> %s ?label
		FILTER regex(str(?label), "http://dbpedia.org/resource/", "i")
		}
		"""%(link,predicado))
		sparql.setReturnFormat(JSON)
		return sparql.query().convert()
	def ConsuDbpediaExtraLabel(self,link,predicado):
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
	def TipoEntidad(self,tiposent):
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

		if tipoMeclado!='' and TipoFinal=='Sin Tipo':
			TipoFinal=tipoMeclado
		return TipoFinal
	def eliminasignos(self,text ):
	        return re.sub('[%s]' % re.escape(string.punctuation), '', text)
	def SelecionaTipo(self,listaTipos,contexto):
		listafrec=[]
		for link in listaTipos:
			try:
				LabelsExtraidos=self.ConsuDbpediaExtraLabel(link[0],'rdfs:label')
			except Exception, e:
				#print e
				continue
			LabelsExtraidos=LabelsExtraidos["results"]["bindings"]
			labels=(' '.join(self.eliminasignos(c["label"]["value"]) for c in LabelsExtraidos)).lower().split(' ')
			labelsSinDuplicados=list(set(labels))
			count=0
			for label in labelsSinDuplicados:
				if label in self.eliminasignos(contexto.lower()).split(' '):
					count=count+1

			listafrec.append([count,link[0],link[1]])
		ListaOrdenado= sorted(listafrec,key=lambda x:x[0], reverse=True)
		return ListaOrdenado


		#entidad= unicodedata.normalize('NFKD', str(entidad)).encode('ascii','ignore') #normaliza la codificacion del texto

	def Linkear(self,entidad,contexto,idioma):
		linkear=[]
		entidad=entidad.decode('utf-8')
		try:
			results = self.ConsuDbpedia(entidad,'rdfs:label',idioma)
			#results = self.ConsuDbpedia(entidad,'rdfs:label','en')
			if results["results"]["bindings"]==[]:
				if idioma=='en':
					results = self.ConsuDbpedia(entidad,'rdfs:label','es')
				else:
					results = self.ConsuDbpedia(entidad,'rdfs:label','en')
		except Exception, e:
			print e
			return
		for result in results["results"]["bindings"]:
			link=(result["label"]["value"])
			print link
			if 'Category' in link:
				continue
			try:
				results2 = self.ConsuDbpedia2(link,'rdf:type')
			except Exception, e:
				continue

			results2 = results2["results"]["bindings"]
			if results2 ==[]:
				UrlyTipo=[]
				results3=self.ConsuDbpedia3(link,'dbpedia-owl:wikiPageDisambiguates')
				results3=results3["results"]["bindings"]
				if results3!=[]:
					for result3 in results3:
						link=(result3["label"]["value"])
						if 'Category:' in link:
							continue
						try:
							results4 = self.ConsuDbpedia2(link,'rdf:type')
						except Exception, e:
							#print e
							continue
						
						results4 = results4["results"]["bindings"]
						TipoFinal=self.TipoEntidad(results4)
						UrlyTipo.append([link,TipoFinal])
					linkear=self.SelecionaTipo(UrlyTipo,contexto)
				else:
					TipoFinal=self.TipoEntidad(results2)
					linkear=[[1,link,TipoFinal]]

			else:
				TipoFinal=self.TipoEntidad(results2)
				linkear=[[1,link,TipoFinal]]
			break
		LisDesyEnlase=[entidad,linkear]
		return LisDesyEnlase

	def DesamEnlaceDescom(self,Entrada):
		DesamEnl=[]
		paraidioma=' '.join(entidad[1] for entidad in Entrada)
		gs = goslate.Goslate()	
		idioma=gs.detect(paraidioma)	
		for entidad in Entrada:
			entidades=' '.join(c[0] for c in entidad[0])
			contexto= entidad[1]
			link=self.Linkear(entidades,contexto,idioma)
			DesamEnl.append(link)
		return DesamEnl
	def DesamEnlace(self,Entrada):
		DesamEnl=[]
		if type(Entrada) is str:
			gs= goslate.Goslate()
			idioma=gs.detect(Entrada)
			lenguajes={"auto":"Detect language","af":"Afrikaans","sq":"Albanian","ar":"Arabic","hy":"Armenian","az":"Azerbaijani","eu":"Basque","be":"Belarusian","bn":"Bengali","bs":"Bosnian","bg":"Bulgarian","ca":"Catalan","ceb":"Cebuano","zh-CN":"Chinese","hr":"Croatian","cs":"Czech","da":"Danish","nl":"Dutch","en":"English","eo":"Esperanto","et":"Estonian","tl":"Filipino","fi":"Finnish","fr":"French","gl":"Galician","ka":"Georgian","de":"German","el":"Greek","gu":"Gujarati","ht":"Haitian Creole","ha":"Hausa","iw":"Hebrew","hi":"Hindi","hmn":"Hmong","hu":"Hungarian","is":"Icelandic","ig":"Igbo","id":"Indonesian","ga":"Irish","it":"Italian","ja":"Japanese","jw":"Javanese","kn":"Kannada","km":"Khmer","ko":"Korean","lo":"Lao","la":"Latin","lv":"Latvian","lt":"Lithuanian","mk":"Macedonian","ms":"Malay","mt":"Maltese","mi":"Maori","mr":"Marathi","mn":"Mongolian","ne":"Nepali","no":"Norwegian","fa":"Persian","pl":"Polish","pt":"Portuguese","pa":"Punjabi","ro":"Romanian","ru":"Russian","sr":"Serbian","sk":"Slovak","sl":"Slovenian","so":"Somali","es":"Spanish","sw":"Swahili","sv":"Swedish","ta":"Tamil","te":"Telugu","th":"Thai","tr":"Turkish","uk":"Ukrainian","ur":"Urdu","vi":"Vietnamese","cy":"Welsh","yi":"Yiddish","yo":"Yoruba","zu":"Zulu","af":"Afrikaans","sq":"Albanian","ar":"Arabic","hy":"Armenian","az":"Azerbaijani","eu":"Basque","be":"Belarusian","bn":"Bengali","bs":"Bosnian","bg":"Bulgarian","ca":"Catalan","ceb":"Cebuano","zh-CN":"Chinese (Simplified)","zh-TW":"Chinese (Traditional)","hr":"Croatian","cs":"Czech","da":"Danish","nl":"Dutch","en":"English","eo":"Esperanto","et":"Estonian","tl":"Filipino","fi":"Finnish","fr":"French","gl":"Galician","ka":"Georgian","de":"German","el":"Greek","gu":"Gujarati","ht":"Haitian Creole","ha":"Hausa","iw":"Hebrew","hi":"Hindi","hmn":"Hmong","hu":"Hungarian","is":"Icelandic","ig":"Igbo","id":"Indonesian","ga":"Irish","it":"Italian","ja":"Japanese","jw":"Javanese","kn":"Kannada","km":"Khmer","ko":"Korean","lo":"Lao","la":"Latin","lv":"Latvian","lt":"Lithuanian","mk":"Macedonian","ms":"Malay","mt":"Maltese","mi":"Maori","mr":"Marathi","mn":"Mongolian","ne":"Nepali","no":"Norwegian","fa":"Persian","pl":"Polish","pt":"Portuguese","pa":"Punjabi","ro":"Romanian","ru":"Russian","sr":"Serbian","sk":"Slovak","sl":"Slovenian","so":"Somali","es":"Spanish","sw":"Swahili","sv":"Swedish","ta":"Tamil","te":"Telugu","th":"Thai","tr":"Turkish","uk":"Ukrainian","ur":"Urdu","vi":"Vietnamese","cy":"Welsh","yi":"Yiddish","yo":"Yoruba","zu":"Zulu"}
			idiomaCompleto=lenguajes[idioma]

			if idioma =='es' or idioma == 'en':
				Entrada=ObjExt.recuperarEntidadesEs(Entrada)
				DesamEnl=self.DesamEnlaceDescom(Entrada)
			else:
				mensaje='El idioma %s no es soportado'%idiomaCompleto
				#print mensaje
				mensaje=gs.translate(mensaje, idioma)
				#print mensaje
				DesamEnl=[]
		elif type(Entrada) is list:
			DesamEnl=self.DesamEnlaceDescom(Entrada)
		else:
			mensaje='Tipo de datos no soportados'
			#print mensaje
			DesamEnl=[]
		
		return DesamEnl

