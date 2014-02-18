## If you put the jar in a non-standard location, you need to
## prepare the CLASSPATH **before** importing jnius
import os
os.environ['CLASSPATH'] = "/home/reroes/Documentos/data_metadata_file/tika_examples/tika-app-1.4.jar"

from jnius import autoclass

## Import the Java classes we are going to need
Tika = autoclass('org.apache.tika.Tika')
Metadata = autoclass('org.apache.tika.metadata.Metadata')
FileInputStream = autoclass('java.io.FileInputStream')
InputStream = autoclass('java.io.InputStream')
Url = autoclass('java.net.URL')
AutoDetectParser= autoclass('org.apache.tika.parser.AutoDetectParser')
BodyContentHandler = autoclass('org.apache.tika.sax.BodyContentHandler')

tika = Tika()
meta = Metadata()

#text = tika.parseToString(FileInputStream("Plan_de_Trabajo_MISW_2013_14_v3.doc"), meta)


#f = FileInputStream("Plan_de_Trabajo_MISW_2013_14_v3.doc")

#InputStream response = new URL(url).openStream();

#url = Url("http://ocw.mit.edu/courses/materials-science-and-engineering/3-024-electronic-optical-and-magnetic-properties-of-materials-spring-2013/study-materials/MIT3_024S13_study1.pdf")
#url = Url("http://ocwus.us.es/ciencias-y-tecnicas-historiograficas/historia-del-libro-impreso/ciencias-y-tecnicas-historiograficas/historia-del-libro-impreso/temas/Tema1/tema-1-el-libro-concepto-y-posibilidades-estudio.pdf")
try:
    url = Url("http://www2.nd.edu/Departments/Maritain/etext/gc1_38.htm")
    f = url.openStream()
    print f
    parser = AutoDetectParser();
    handler = BodyContentHandler()
    parser.parse(f,handler,meta)
    print meta
    print meta.__class__
    print meta.names()
    for m in meta.names():
        print m, meta.get(m)
    #print text
except:
    print "error --- url ---:", url
