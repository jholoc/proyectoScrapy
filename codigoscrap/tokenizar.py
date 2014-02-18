#!/usr/bin/env python
#-*-coding: utf-8 *
import nltk
from nltk import RegexpParser,sent_tokenize, word_tokenize, pos_tag, ne_chunk
import goslate

def traducir(token, token2):
	gs = goslate.Goslate()
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

def tagear(tags):
	tags=word_tokenize(tags)
	#print tags
	#for i in gs.translate(tags, 'en'):
	#	print(i)
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

    #(r'.*', 'NN')
	]
	regexp_tagger = nltk.RegexpTagger(patterns)
	for index,t in enumerate(tags):
		newtag=regexp_tagger.tag(nltk.word_tokenize(t))
		if newtag[0][1]!=None:
			t=newtag[0]
			tags[index]=newtag[0]
		else:
			if index+1<len(tags):
				tTra=traducir(t,tags[index+1])
			else:
				tTra=traducir(t,tags[index])
			nuevotag=pos_tag(nltk.word_tokenize(tTra))[0]
			#print nuevotag
			nuevotag=(t,nuevotag[1])
			tags[index]=nuevotag
	return tags


gs = goslate.Goslate()
palabra=gs.translate('ha de ser ', 'en')
print palabra

texto="""was El monte Fuji ya es Patrimonio de la Humanidad. El volcán Fuji, icono de Japón, entró este sábado a formar parte del patrimonio mundial o de la humanidad de la Organización de las Naciones Unidas para la Educación, la Ciencia y la Cultura (Unesco). El Comité del Patrimonio Mundial reunido en Phnom Penh alabó esta cumbre de 3.776 metros de altura que "ha sido inspiración de poetas y artistas y ha sido objeto de peregrinación desde hace siglos". Los japoneses consideran sagrado el Fujiyama (monte Fuyi en japonés), el punto más alto del país, y miles viajan todos los veranos allí para subir a la cumbre, porque es la única época del año que el tiempo lo permite. Los expertos de la Unesco también inscribieron en el patrimonio de la humanidad hoy las terrazas de arroz de Honghe Hani, en China, y el Parque Nacional Sehlabathebe, en Lesoto. Las terrazas de arroz de Hongye Hani cubren 16.603 hectáreas en la provincia de Yunnan y presentan desde hace 1.300 años un paisaje espectacular de arrozales que descienden de manera escalonada desde las montañas Ailao hasta la ribera del río Hong. La Unesco incorporó en la lista 6.550 hectáreas del Parque Nacional Sehlabathebe, en Lesoto, como una extensión de la reserva uKhahlamba Drakensberg, en Sudáfrica. El Comité del Patrimonio Mundial comenzó el pasado día 16 una serie de sesiones en Phnom Penh para examinar 32 candidaturas y clausurará las reuniones el próximo día 27 en el marco de los templos de Angkor, joya arquitectónica del imperio Jemer, en el norte de Camboya. El organismo también ha analizado o analizará el estado de conservación de lugares declarados patrimonio de la humanidad en Siria y Mali, afectados por la guerra, así como el Parque de Doñana, en España, y el casco histórico de Valparaíso, en Chile. EFE
"""
#texto=
''' : jun. 2012
Q/A - European Language Technology Industries
author: Jochen Hummel, ESTeam AB
author: László Podhorányi, Vodafone Hungary
author: Johannes Bursch, Daimler AG
author: Laszlo Tihanyi, MorphoLogic Kft.
author: Rose Lockwood, INMARK International Area
published: Jan. 9, 2012,   recorded: June 2011,   views: 16
Categories
Top » Computer Science » Computational Linguistics'''
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
	#print parsed
	for chunk in parsed:
		#print chunk
		#if hasattr(chunk, 'node'):
		#	print chunk.node
		if hasattr(chunk, 'node'):
			#	print chunk	
			#print chunk.leaves()
			#print ' '.join(c[0] for c in chunk.leaves())
			Lista.append (' '.join(c[0] for c in chunk.leaves()))
for c in sorted(Lista):
	print c 
			#entities.extend([chunk for chunk in chunks if hasattr(chunk, 'node')])"""