#!/usr/bin/env python
#-*-coding: utf-8 *
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import *
from nltk.probability import *
import codecs
import unicodedata
import nltk.chunk
import itertools

from nltk import RegexpParser
from nltk.corpus import cess_esp as cess
from nltk import UnigramTagger as ut
from nltk import BigramTagger as bt
from nltk.corpus import cess_esp
from dateutil import parser #para fechas
from dateutil.parser import parse


from nltk.tag import RegexpTagger, UnigramTagger
from nltk.corpus import brown

from textblob import TextBlob
#from xgoogle.translate import Translator
import goslate


#print parse('20 de diciembre del 2001',parserinfo=SpanishParserInfo())

print parse(" 2008-06-29 en el Centro de Convenciones de la Universidad", fuzzy=True)
print parse("30 de enero de 1990", fuzzy=True)
print parse("Tcnica Particular de Loja, June", fuzzy=True)
print parse("La noche", fuzzy=True)

#texto = str(DBconex.extraertexto())  #extracion de las noticias de la base datos
texto = ' coordinado por la Universidad Federal de Rio de Janeiro – Brasil. se con whith El Centro de Convenciones de la Universidad Técnica Particular de Loja, June, 2008-06-29 la Compañía de Teatro de la UTPL, College of Physicians presento el estreno de Puebla de las Mujeres bajo la direccion de Alain Chaviano Aldonza, es una obra teatral del genero de la comedia escrito por los brothers brother siblings hermanos Alvarez Quintero y estrenada en 1912.uesta en escena. El escenario estuvo ambientado en la epoca, 1912, simulaba la sala de la casa del cura parroco del pueblo junto a las luces y la musica transportaron a los asistentes a aquella epoca. Los actores fueron a pareciendo en escena de acuerdo al desarrollo de la historia, haciendo reir y divertir al publico con cada interpretacion. La historia se desarrolla en un pueblo donde mandan y reinan las mujeres como mismo lo menciona dentro de la trama el medico del pueblo, ellas hacen y deshacen a su antojo, siendo su único objetivo casar a todas las muchachas del pueblo con todos los hombres que llegan a el. thus asi Asi llega al pueblo el abogado Adolfo Adalid un muchacho apuesto y galante, cuyo error al llegar fue haber visto a una de las muchachas del Pueblo, Juanita la Rosa, desde ese momento todas se empeniaran en terminar casandolo con ella. Concha Puerto es una mujer muy impetuosa, entrometida en todo lo que no le importa, hara lo imposible para lograr que el abogado se interese por Juanita, y para realizar su cometido se valdra de todo y de todos, haciendo que cada situacion sea muy jocosa y entretenida por los enredos que ella genera. Andrea Pazminio, actriz, interpreta a Concha Puerto lleva ocho anios dentro de la Compania y nos comenta el teatro para mi es otro mundo, es meterse en otro papel y algo increible para cada actor. Con cada obra que realizo quiero dejar un mensaje a la gente, en esta ocasión Puebla de las Mujeres se asemeja al entorno lojano donde a las mujeres les gusta mandar, es una obra bien simpatica, fresca y sobre todo la gente vive muy estresada y con esta obra lograremos sacar una sonrisa a todo el publico indica Alain Chaviano, Director de la Compania de Teatro de la UTPL. Esta noche podremos disfrutar nuevamente de esta maravillosa obra a las 19h00 en el Centro de Convenciones de la UTPL, la entrada es gratuita.En el mes de noviembre del 2012, se dio a conocer el  Proyecto BABEL en co-ordinación con la UTPL,  que extendió la cordial invitación para la postulación de Becas a Europa, para Licenciatura, Master, Doctorado, Postdoctorado, Personal Académico y Administrativo. Dado que La Universidad Técnica Particular de Loja, es miembro asociado del Proyecto de la Unión Europea – Erasmus Mundus “BABEL” Building academic bounds between Europe and Latin American, coordinado por la Universidad de Porto – Portugal y co- coordinado por la Universidad Federal de Rio de Janeiro – Brasil. Por tal motivo más de 20 ex alumnos de las distintas Titulaciones de la UTPL, aplicaron para las becas del Proyecto Babel, siendo una  gran oportunidad por los beneficios que otorga y oferta el proyecto BABEL, se hacen visibles en montos de dinero que cubren los gastos de estudio en las universidades a postular y  son: licenciaturas (mil euros), doctorados (1.500), post doctorados (1.800) y personal académico y administrativo (2.500). Además  cubrirá gastos de ida y vuelta, seguro de vida y se efectuará conjuntamente con el postulante el proceso de visado y el seguimiento durante el ciclo de estudios. La divulgación de los resultados será en abril de este año, por lo cual deseamos la mejor de las suertes a nuestros ex alumnos postulantes.'
texto="""En el museo de Arqueología y Lojanidad de la UTPL, estarán expuestas  las fotografías del ecuatoriano Pablo Palacios, en la muestra titulada: Las Cuatro Estaciones del Central Park de Nueva York.

La exposición cuenta con 60 fotografías tomadas durante los últimos tres años y que muestran al parque más grande de Nueva York en sus cuatro estaciones.  Su objetivo es concienciar a los estudiantes sobre el cuidado del medio ambiente, además de fomentar el intercambio cultural entre ambos países.

El 4 de diciembre se llevó a cabo la inauguración con la presencia de Robert McInturff, agregado cultural de la Embajada de los Estados Unidos en Quito, quien habló sobre la importancia que tiene fraternizar con el pueblo ecuatoriano, ya que se puede llevar a cabo proyectos como becas  e intercambios culturales.

El Central Park ha sido escogido como  punto para fotografiar, ya que es considerado como los pulmones de Nueva York. Es un lugar lleno de vitalidad, donde se puede observar gente paseando en bicicleta, personas mayores caminando y niños jugando.

Este parque, que es uno de los más grandes del mundo, cuenta con lagos artificiales, praderas, un zoológico y tiendas. Recibe  más de 20 millones de visitantes cada año.

pesinche@utpl.edu.ec"""
cess_sents = cess.tagged_sents()

# Train the unigram tagger
uni_tag = ut(cess_sents)

sentence = "caminar caminando caminara correr aprender aprendio conocer  caminar, correr, escalar, saltar y explorar"

# Tagger reads a list of tokens.
#print nltk.corpus.cess_esp.words() 
nltk.corpus.cess_esp.tagged_words()
#print uni_tag.tag(texto.split(" "))




#print pos_tag(word_tokenize('caminar caminando caminara correr aprender aprendio conocer  caminar, correr, escalar, saltar y explorar'))
#print stopwords.words('spanish')
#archivo=codecs.open("contenidonoticia.txt","r",encoding="utf-8")
#texto = archivo.read()
#texto = unicodedata.normalize('NFKD', texto).encode('ascii','ignore')#normailza texto: elimina caracteres especiales
def tokenizar(texto):
	token = nltk.word_tokenize(texto) #tokeniza los contenidos de las noticias
	filtered_words = [w for w in token if not w.lower() in stopwords.words('spanish')]
	return filtered_words
def extract_entities(text):
	entities = []
	for sentence in sent_tokenize(text):
	    chunks = ne_chunk(pos_tag(word_tokenize(sentence)))
	    entities.extend([chunk for chunk in chunks if hasattr(chunk, 'node')])
	return entities

def extract_entities2(text):
	entities = []
	
	"""t0 = nltk.DefaultTagger('NN')
	t1 = nltk.UnigramTagger(train_sents, backoff=t0)
	t2 = nltk.BigramTagger(train_sents, backoff=t1)
	t2.evaluate(test_sents)"""
	
	for sentence in sent_tokenize(text):
	    #print pos_tag(nltk.word_tokenize(sentence))
	    print sentence
	    tags=pos_tag(nltk.word_tokenize(sentence))
	    tags=tagear(tags)
	    chunks = ne_chunk(pos_tag(nltk.word_tokenize(sentence)))
	    #chunks = ne_chunk(regexp_tagger.tag((nltk.word_tokenize(text))))
	    chunks = ne_chunk(tags)
	    #chunks.draw()
	    #print chunks
	    for chunk in chunks:
	    	#print chunk
	    	#if hasattr(chunk, 'node'):
	    	#	print chunk.node
	    	if hasattr(chunk, 'node') :
	    		print chunk	
	    		entities.extend([chunk for chunk in chunks if hasattr(chunk, 'node')])
	return entities

def entities(text):
    chunks = \
        ne_chunk(
            pos_tag(
                word_tokenize(text)),
        binary=True) # binary only enables one type, "NE"
    return chunks 

def tagear(tags):
	tags=word_tokenize(tags)
	print tags
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
    (r'^(de|De|con|Con|En|en|\xe2\x80\x93)$', 'IN'),
    (r'^(A|A|(a|A)nte|(b|B)ajo|(c|C)on|(c|C)ontra|(d|D)esde|(e|E)n|(e|E)ntre|(h|H)acia|(h|H)asta|(p|P)ara|(p|P)or|(s|S)egún|(s|S)in|(s|S)obre|(t|T)ras)$', 'IN'),
    (r'^(el|El|EL|Los|los|la|La|Las|las|del)$', 'DT'),
    (r'^(éste|Éste|ésta|Ésta|esto|Esto|éstos|Éstos|éstas|Éstas|ése|Ése|ésa|Ésa|eso|Eso|ésos|Ésos|ésas|Ésas|áquel|Áquel|áquella|Áquella|aquello|Aquello|áquellos|Áquellos|áquellas|Áquellas)$', 'PRP'),
    (r'^(este|Este|esta|Esta|esto|Esto|estos|Estos|estas|Estas|ese|Ese|esa|Esa|eso|Eso|esos|Esos|esas|Esas|aquel|Aquel|aquella|Aquella|aquello|Aquello|aquellos|Aquellos|aquellas|Aquellas)$', 'DT'),
    (r'^(yo|Yo|tú|Tú|tu|él|Él|Ella|ella|nosotros|Nosotros)$', 'PRP'),
    (r'^(Así|Asi|asi|así|más|Más)$','RB'),
    (r'^(Así|Asi|asi|así|más|Más)$','RB'),
    (r'^(Y|y|o|O|U|u|ni|Ni)$','CC'),
    (r'^(véase)$','VR'),
    (r'^(admitir|afectar|estar|apuntar|permitir|responder|aparecer|aplicar|discutir|arreglar|consertar|llegar|preguntar|atacar|evitar|basarse|vencer|apanar|volverse|empezar|creer|pertenecer|romper|construir|quemar|comprar|llamar|poder|importar|cargar|llevar|atrapar|causar|cambiar|cobrar|comprobar|controlar|elejir|reclamar|limpiar|despejar|trepar|cerrar|recolectar|come|venir|cometer|comparar|reclamar|completar|concernir|confirmar|conectar|considerar|consistir|contactar|contenet|continuar|contribuir|controlar|cocinar|copiar|corregir|costar|contar|covertir|crear|cruzar|llorar|cortar|dañar|bailar|repartir|decidir|entregar|exigir|denegar|depender|describir|diseñar|destruir|desarrollar|morir|desaparecer|descubrir|discutir|dividir|dormir|hacer|dibujar|vistirse|beber|manejar|dejar|caer|atar|comer|habilitar|dar|coraje|disfrutar|examinar|existir|esperar|experimentar|explicar|expresar|ampliar|encarar|reprobar|calentar|ajustarse|alimentar|sentir|pelear|llenar|rellenar|encontrar|acabar|terminar|quedar|volar|doblar|seguir|forzar|olvidar|olvidar|formar|adquirir|conseguir|obtener|comprar|llevar|dar|ir|crecer|manejar|suceder|odiar|detestar|tener|dirigirse|oir|ayudar|ocultar|golpear|agrarrar|coger|esperar|herir|identificar|imaginar|mejorar|incluir|incremetar|indicar|infuenciar|informar|tener|intención|introducir|invitar|encolver|unir|unirse|saltar|quedarse|patear|matar|tocar|saber|conocer|durar|reir|echarse|dirigir|aprender|dejar|irse|prestar|dejar|mentir|gustar|limitar|unir|relacionar|oir|vivir|mirar|perder|amar|hacer|administrar|marcar|importar|quizas|significar|querer|decir|medir|comprender|encontrase|meditar|mencionar|tener|contar|extrañar|perder|mover|necesitar|notar|obtener|ocurrir|ofrecer|abrir|ordenar|tener|pasar|pagar|rendir|realizar|escoger|elegir|colocar|planear|jugar|apuntar|preferir|preparar|presentar|presionar|prevenir|producir|prometer|proteger|probar|proveer|publicar|jalar|empujar|colocar|poner|levantar|alcanzar|leer|darse|cuenta|recibir|reconocer|grabar|reducir|referir|reflexionar|reflejar|rechazar|eliminar|bostezar|brillar|brindar|bromear|broncearse|bucear|burlarse|Buscar|cabalgar|viajar|Caber|ENTRAR|pode|caber|adaptarse|celebrar|caerse|calarse|mojarse|Calcular|CALENTAR|Calificar|marcar|callar|dejar|hablar|decir|Calmar|Caminar|Cancelar|cansar|cansarse|cantar|carecer|Cargar|casarse|Cascar|Castigar|Cazar|Celebrar|CENAR|cepillar|cerrar|certificar|charlar|Chillar|chocar|chupar|circular|citar|concertar|Clasificar|clavar|cobrar|cargar|cocer|Cocinar|coger|colocar|colar|colarse|COLGAR|combinar|Comenzar|empezar|Compartir|compartir|comprar|comprender|Comunicar|concluir|terminar|Conducir|Confiar|Confundiste|cometer|CONOCER|saber|conseguir|obtener|lograr|Conservar|Construir|Consultar|Consumir|Contar|contemplate|contestar|responder|Continuar|contradecir|contribuir|convencer|correr|Cortar|costar|CREAR|CRECER|CREER|pensar|criticar|Cruzar|CUIDAR|cumplir|llevar|cumplir|Curar|dar|Deber|Decir|decorar|Dedicar|dedicarse|hacer|ganar|defender|dejar|prestar|tomar|deletrear|Denegar|rechazar|desayunar|descalzarse|quitarse|Descansar|desconectar|apagar|descontar|dar|describir|Descubrir|desear|desnudar|desobedecer|despedir|ver|despedirse|Despegar|desordenar|meter|despertarse|destacar|señalar|destruir|destrozar|desvestir|desvestirse|desviar|Detener|Devolver|Dibujar|dictar|diluir|disolver|adelgazar|dimitir|renunciar|dirigir|gestionar|disculpar|perdonar|disculparse|pedir|discutir|discutir|argumentar|diseñar|disfrazarse|vestir|Disfrutar|disgustarse|molestarse|Disminuir|reducir|disparar|investigaciones|distinguir|distraer|mantener|entreter|Distribuir|divertir|divertirse|divorciar|Doblar|doler|Dormir|ducharse|Dudar|poner|Durar|echar|lanzar|Editar|publicar|elaborar|producir|preparar|Elegir|elevar|aumentar|Eliminar|embarcar|emprender|Emigrar|emitir|transmitir|emocionarse|mueve|empaquetar|empacar|empatar|igualar|Empezar|emplear|empujar|impulsar|enamorarse|encantar|amar|encargar|pedir|encender|Desactivación|enchufar|conectar|encontrar|enfadarse|enojarse|enfocar|centrarse|enfriar|enganchar|engañar|mentir|engordar|enrollar|ensanchar|ampliar|ensayar|Enseñar|ensuciar|entendre|enterarse|averiguar|ENTRAR|ir|Entrenar|capacitar|Entregar|entretener|envejecer|envidiar)$','VB')

    #(r'.*', 'NN')
	]
	regexp_tagger = nltk.RegexpTagger(patterns)
	for index,t in enumerate(tags):
		#print t
		newtag=regexp_tagger.tag(nltk.word_tokenize(t))
		if newtag[0][1]!=None:
			#print newtag[0]
			t=newtag[0]
			tags[index]=newtag[0]
		else:
			tTra=traducir(t,tags[index])
			#print tags[index]
			nuevotag=pos_tag(nltk.word_tokenize(tTra))[0]
			print nuevotag
			#print nuevotag[0]
			#print t
			#nuevotag[0]=t
			nuevotag=(t,nuevotag[1])
			#print nuevotag
			tags[index]=nuevotag
	#print tags		
	return tags
def traducir(token, token2):
	gs = goslate.Goslate()
	#print token
	if len(token)>2:
		token=gs.translate(token, 'en')
	else:
		token= gs.translate(token+' '+token2, 'en')
		print token
		token=word_tokenize(token)
		token=token[0]
	token=word_tokenize(token)
	token=token[len(token)-1]
	#print token
	return token

def sentimentanalysis(texto):
	testimonial = TextBlob(texto)
	for zen in testimonial.words:
		print zen.translate(to="en")


chunker = RegexpParser("""
ENTI:
    {<NNP|NNPS>+<NNP|NNPS|NN|NNS>}  # Nouns and Adjectives, terminated with Nouns
    {<NNP|NNPS><IN><NNP|NNPS>}
    {<NNP|NNPS>}
ENTIDACOMP:
	{<DT><NN|NNS><ENTI>}
	{<DT><NN|NNS><IN><ENTI>}
	{<ENTI><IN><ENTI>}	
    {<ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP>}  # Above, connected with in/of/etc...
    {<ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP>}
ENTIDACOMP2:
	{<ENTI|ENTIDACOMP><IN><ENTI|ENTIDACOMP>}
    

""")
"""
NBAR:
    {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
NP:

    {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc... """
#sentimentanalysis("su")
print 'asadasdasdasdsadadsa'
gs = goslate.Goslate()
palabra=gs.translate('sido ', 'en')
print palabra

print 'asdasdsadasdadsadadsadsa'

for sentence in sent_tokenize(texto):
	tags=tagear(sentence)
	#tags=tagear(traducir(word_tokenize(sentence)))
	#print tags
	parsed = chunker.parse(tags)
	print parsed
	"""for chunk in parsed:
		#print chunk
		#if hasattr(chunk, 'node'):
		#	print chunk.node
		if hasattr(chunk, 'node'):
			print chunk	
			#entities.extend([chunk for chunk in chunks if hasattr(chunk, 'node')])"""

