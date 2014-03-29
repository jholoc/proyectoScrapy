#!/usr/bin/env python
#-*-coding: utf-8 *
import nltk
from nltk import RegexpParser,sent_tokenize, word_tokenize, pos_tag, ne_chunk
import goslate
gs = goslate.Goslate()
class Tokenizar():
	def traducir(self,token, token2):
		#print token
		if len(token)>2:
			tokenTra=gs.translate(token, 'en')
		else:
			#tokenTra= gs.translate(token+' '+token2, 'en')
			tokenTra= gs.translate(token+' '+token+' '+token+' '+token, 'en')
			#print tokenTra
			tokenTra=word_tokenize(tokenTra)
			tokenTra=tokenTra[0]
		tokenTra=word_tokenize(tokenTra)
		tokenTra=tokenTra[len(tokenTra)-1]
		#print tokenTra
		if token.islower()==True:
			tokenTra=tokenTra.lower()
		return tokenTra
	def tagearSentenciaEs(self,tags):
		tags=word_tokenize(tags)
		patterns = [
	    (r'^@\w+', 'NNP'),
	    (r'^\d+$', 'CD'),
	    (r'.*ing$', 'VBG'),
	    (r'.*ment$', 'NN'),
	    (r'.*ful$', 'JJ'),
	    (r'la', 'IN'),
	    (r'La', 'IN'),
	    (r'de', 'IN'),
	    (r'el', 'IN'),
	    #(r'.*', 'NN')
		]
		patterns = [
		(r'^,$', ','),
		(r'^;$', ';'),
		(r'^:$', ':'),
		(r'^\.$', '.'),
		(r'^-$', '-'),
		(r'^/$', '/'),
		(r'^\($', '('),
		(r'^\)$', ')'),
		(r'^\–$', '-'),
	    (r'^(de|De|con|Con|En|en|\xe2\x80\x93)$', 'IN'),
	    (r'^(A|A|(a|A)nte|(b|B)ajo|(c|C)on|(c|C)ontra|(d|D)esde|(e|E)n|(e|E)ntre|(h|H)acia|(h|H)asta|(p|P)ara|(p|P)or|(s|S)egún|(s|S)in|(s|S)obre|(t|T)ras)$', 'IN'),
	    (r'^(el|El|EL|Los|los|la|La|Las|las|del)$', 'DT'),
	    (r'^(éste|Éste|ésta|Ésta|esto|Esto|éstos|Éstos|éstas|Éstas|ése|Ése|ésa|Ésa|eso|Eso|ésos|Ésos|ésas|Ésas|áquel|Áquel|áquella|Áquella|aquello|Aquello|áquellos|Áquellos|áquellas|Áquellas)$', 'PRP'),
	    (r'^(este|Este|esta|Esta|esto|Esto|estos|Estos|estas|Estas|ese|Ese|esa|Esa|eso|Eso|esos|Esos|esas|Esas|aquel|Aquel|aquella|Aquella|aquello|Aquello|aquellos|Aquellos|aquellas|Aquellas)$', 'DT'),
	    (r'^(yo|Yo|tú|Tú|tu|él|Él|Ella|ella|nosotros|Nosotros)$', 'PRP'),
	    (r'^(Así|Asi|asi|así|más|Más)$','RB'),
	    (r'^(Así|Asi|asi|así|más|Más)$','RB'),
	    (r'^(Y|y|o|O|U|u|ni|Ni|ya|Ya)$','CC'),
	    (r'^(véase)$','VR'),
	    (r'^(admitir|afectar|estar|apuntar|permitir|responder|aparecer|aplicar|discutir|arreglar|consertar|llegar|preguntar|atacar|evitar|basarse|vencer|apanar|volverse|empezar|creer|pertenecer|romper|construir|quemar|comprar|llamar|poder|importar|cargar|llevar|atrapar|causar|cambiar|cobrar|comprobar|controlar|elejir|reclamar|limpiar|despejar|trepar|cerrar|recolectar|come|venir|cometer|comparar|reclamar|completar|concernir|confirmar|conectar|considerar|consistir|contactar|contenet|continuar|contribuir|controlar|cocinar|copiar|corregir|costar|contar|covertir|crear|cruzar|llorar|cortar|dañar|bailar|repartir|decidir|entregar|exigir|denegar|depender|describir|diseñar|destruir|desarrollar|morir|desaparecer|descubrir|discutir|dividir|dormir|hacer|dibujar|vistirse|beber|manejar|dejar|caer|atar|comer|habilitar|dar|coraje|disfrutar|examinar|existir|esperar|experimentar|explicar|expresar|ampliar|encarar|reprobar|calentar|ajustarse|alimentar|sentir|pelear|llenar|rellenar|encontrar|acabar|terminar|quedar|volar|doblar|seguir|forzar|olvidar|olvidar|formar|adquirir|conseguir|obtener|comprar|llevar|dar|ir|crecer|manejar|suceder|odiar|detestar|tener|dirigirse|oir|ayudar|ocultar|golpear|agrarrar|coger|esperar|herir|identificar|imaginar|mejorar|incluir|incremetar|indicar|infuenciar|informar|tener|intención|introducir|invitar|encolver|unir|unirse|saltar|quedarse|patear|matar|tocar|saber|conocer|durar|reir|echarse|dirigir|aprender|dejar|irse|prestar|dejar|mentir|gustar|limitar|unir|relacionar|oir|vivir|mirar|perder|amar|hacer|administrar|marcar|importar|quizas|significar|querer|decir|medir|comprender|encontrase|meditar|mencionar|tener|contar|extrañar|perder|mover|necesitar|notar|obtener|ocurrir|ofrecer|abrir|ordenar|tener|pasar|pagar|rendir|realizar|escoger|elegir|colocar|planear|jugar|apuntar|preferir|preparar|presentar|presionar|prevenir|producir|prometer|proteger|probar|proveer|publicar|jalar|empujar|colocar|poner|levantar|alcanzar|leer|darse|cuenta|recibir|reconocer|grabar|reducir|referir|reflexionar|reflejar|rechazar|eliminar|bostezar|brillar|brindar|bromear|broncearse|bucear|burlarse|Buscar|cabalgar|viajar|Caber|ENTRAR|pode|caber|adaptarse|celebrar|caerse|calarse|mojarse|Calcular|CALENTAR|Calificar|marcar|callar|dejar|hablar|decir|Calmar|Caminar|Cancelar|cansar|cansarse|cantar|carecer|Cargar|casarse|Cascar|Castigar|Cazar|Celebrar|CENAR|cepillar|cerrar|certificar|charlar|Chillar|chocar|chupar|circular|citar|concertar|Clasificar|clavar|cobrar|cargar|cocer|Cocinar|coger|colocar|colar|colarse|COLGAR|combinar|Comenzar|empezar|Compartir|compartir|comprar|comprender|Comunicar|concluir|terminar|Conducir|Confiar|Confundiste|cometer|CONOCER|saber|conseguir|obtener|lograr|Conservar|Construir|Consultar|Consumir|Contar|contemplate|contestar|responder|Continuar|contradecir|contribuir|convencer|correr|Cortar|costar|CREAR|CRECER|CREER|pensar|criticar|Cruzar|CUIDAR|cumplir|llevar|cumplir|Curar|dar|Deber|Decir|decorar|Dedicar|dedicarse|hacer|ganar|defender|dejar|prestar|tomar|deletrear|Denegar|rechazar|desayunar|descalzarse|quitarse|Descansar|desconectar|apagar|descontar|dar|describir|Descubrir|desear|desnudar|desobedecer|despedir|ver|despedirse|Despegar|desordenar|meter|despertarse|destacar|señalar|destruir|destrozar|desvestir|desvestirse|desviar|Detener|Devolver|Dibujar|dictar|diluir|disolver|adelgazar|dimitir|renunciar|dirigir|gestionar|disculpar|perdonar|disculparse|pedir|discutir|discutir|argumentar|diseñar|disfrazarse|vestir|Disfrutar|disgustarse|molestarse|Disminuir|reducir|disparar|investigaciones|distinguir|distraer|mantener|entreter|Distribuir|divertir|divertirse|divorciar|Doblar|doler|Dormir|ducharse|Dudar|poner|Durar|echar|lanzar|Editar|publicar|elaborar|producir|preparar|Elegir|elevar|aumentar|Eliminar|embarcar|emprender|Emigrar|emitir|transmitir|emocionarse|mueve|empaquetar|empacar|empatar|igualar|Empezar|emplear|empujar|impulsar|enamorarse|encantar|amar|encargar|pedir|encender|Desactivación|enchufar|conectar|encontrar|enfadarse|enojarse|enfocar|centrarse|enfriar|enganchar|engañar|mentir|engordar|enrollar|ensanchar|ampliar|ensayar|Enseñar|ensuciar|entendre|enterarse|averiguar|ENTRAR|ir|Entrenar|capacitar|Entregar|entretener|envejecer|envidiar)$','VB')

		]
		regexp_tagger = nltk.RegexpTagger(patterns)
		for index,t in enumerate(tags):
			newtag=regexp_tagger.tag(nltk.word_tokenize(t))
			if newtag[0][1]!=None:
				t=newtag[0]
				tags[index]=newtag[0]
			else:
				if index+1<len(tags):
					tTra=self.traducir(t,tags[index+1])
				else:
					tTra=self.traducir(t,tags[index])
				nuevotag=pos_tag(nltk.word_tokenize(tTra))[0]
				nuevotag=(t,nuevotag[1])
				tags[index]=nuevotag
		return tags

	def tagearSentenciaEn(self,tags):
		tags=word_tokenize(tags)
		tags=pos_tag(tags)
		return tags

	def tagear(self,sentencia):
		idioma=gs.detect(sentencia)
		lenguajes={"auto":"Detect language","af":"Afrikaans","sq":"Albanian","ar":"Arabic","hy":"Armenian","az":"Azerbaijani","eu":"Basque","be":"Belarusian","bn":"Bengali","bs":"Bosnian","bg":"Bulgarian","ca":"Catalan","ceb":"Cebuano","zh-CN":"Chinese","hr":"Croatian","cs":"Czech","da":"Danish","nl":"Dutch","en":"English","eo":"Esperanto","et":"Estonian","tl":"Filipino","fi":"Finnish","fr":"French","gl":"Galician","ka":"Georgian","de":"German","el":"Greek","gu":"Gujarati","ht":"Haitian Creole","ha":"Hausa","iw":"Hebrew","hi":"Hindi","hmn":"Hmong","hu":"Hungarian","is":"Icelandic","ig":"Igbo","id":"Indonesian","ga":"Irish","it":"Italian","ja":"Japanese","jw":"Javanese","kn":"Kannada","km":"Khmer","ko":"Korean","lo":"Lao","la":"Latin","lv":"Latvian","lt":"Lithuanian","mk":"Macedonian","ms":"Malay","mt":"Maltese","mi":"Maori","mr":"Marathi","mn":"Mongolian","ne":"Nepali","no":"Norwegian","fa":"Persian","pl":"Polish","pt":"Portuguese","pa":"Punjabi","ro":"Romanian","ru":"Russian","sr":"Serbian","sk":"Slovak","sl":"Slovenian","so":"Somali","es":"Spanish","sw":"Swahili","sv":"Swedish","ta":"Tamil","te":"Telugu","th":"Thai","tr":"Turkish","uk":"Ukrainian","ur":"Urdu","vi":"Vietnamese","cy":"Welsh","yi":"Yiddish","yo":"Yoruba","zu":"Zulu","af":"Afrikaans","sq":"Albanian","ar":"Arabic","hy":"Armenian","az":"Azerbaijani","eu":"Basque","be":"Belarusian","bn":"Bengali","bs":"Bosnian","bg":"Bulgarian","ca":"Catalan","ceb":"Cebuano","zh-CN":"Chinese (Simplified)","zh-TW":"Chinese (Traditional)","hr":"Croatian","cs":"Czech","da":"Danish","nl":"Dutch","en":"English","eo":"Esperanto","et":"Estonian","tl":"Filipino","fi":"Finnish","fr":"French","gl":"Galician","ka":"Georgian","de":"German","el":"Greek","gu":"Gujarati","ht":"Haitian Creole","ha":"Hausa","iw":"Hebrew","hi":"Hindi","hmn":"Hmong","hu":"Hungarian","is":"Icelandic","ig":"Igbo","id":"Indonesian","ga":"Irish","it":"Italian","ja":"Japanese","jw":"Javanese","kn":"Kannada","km":"Khmer","ko":"Korean","lo":"Lao","la":"Latin","lv":"Latvian","lt":"Lithuanian","mk":"Macedonian","ms":"Malay","mt":"Maltese","mi":"Maori","mr":"Marathi","mn":"Mongolian","ne":"Nepali","no":"Norwegian","fa":"Persian","pl":"Polish","pt":"Portuguese","pa":"Punjabi","ro":"Romanian","ru":"Russian","sr":"Serbian","sk":"Slovak","sl":"Slovenian","so":"Somali","es":"Spanish","sw":"Swahili","sv":"Swedish","ta":"Tamil","te":"Telugu","th":"Thai","tr":"Turkish","uk":"Ukrainian","ur":"Urdu","vi":"Vietnamese","cy":"Welsh","yi":"Yiddish","yo":"Yoruba","zu":"Zulu"}
		idiomaCompleto=lenguajes[idioma]


		if idioma =='es':
			Lista=self.tagearSentenciaEs(sentencia)
		elif idioma == 'en':
			Lista=self.tagearSentenciaEn(sentencia)
		else:
			mensaje='El idioma %s no es soportado'%idiomaCompleto
			print mensaje
			mensaje=gs.translate(mensaje, idioma)
			print mensaje
			Lista=[]
		return Lista
