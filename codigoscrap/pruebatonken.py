#-*- coding: utf-8 -*-
import nltk
s = "Quito is a city of Ecuador"
s = '''Jhonny Zaruma Try entering your own text in this text box to see what knowledge AlchemyAPI can extract from your unstructured data. University Tecnic  of Loja is the university Catolic of Loja'''
a = nltk.word_tokenize(s)
b = nltk.pos_tag(a)
c = nltk.ne_chunk(b)
#print ">>", b
print ">>", c
aaa=type(s).text()
print aaa
print type(b)
print type(c)
for x in c.subtrees():
   #print ">>>" , x
   word = [w[0] for w in x.leaves()]
   tag = x.node
   name = " ".join(word)
   print name +" >> "+ tag
   """if x.node == "NE":
           words = [w[0] for w in x.leaves()]
           name = " ".join(words)
           print name"""

"""for x in c.subtrees():
   if x.node == "NE":
           words = [w[0] for w in x.leaves()]
           name = " ".join(words)
           print name
"""