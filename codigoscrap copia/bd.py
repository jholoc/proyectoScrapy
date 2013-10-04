# -*- coding: utf-8-sig -*-
import codecs
import MySQLdb
from config import *
import MySQLdb as mdb
import unicodedata

class BDdatos():
    """
        Clase para la Base de Datos
    """
    def conectar(self):
        """
           conectarme a la bd
        """
        db = None
        try:
            #obtener datos de autentificacion de la base de datos
            host = HOST
            user = USER
            clave = PASS
            base_datos = BD
            db=MySQLdb.connect(host=host,user=user,passwd=clave,db=base_datos,charset='utf8',use_unicode=True )
        except Exception, e:
            print "error de coneccion", e
        return db
    
    def cerrar(self, db):
        """
            cerrar la base de datos
        """
        db.close()
    
    def datos_start_url(self, tabla):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "select * from %s limit 240000000000;"%tabla
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    def datos_start_url_orden(self, tabla):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "select * from %s ;"%tabla
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    
    def insertar_datos(self, dato1, dato2, dato3,dato4,dato5, tabla):
        db=self.conectar()
        cur=db.cursor()
        cur.execute(u"""INSERT INTO """+ tabla +""" (urlcurso, urlmenu, titulomenu, urloer, titulooer) VALUES (%s, %s, %s,%s, %s)""" ,
            (dato1, dato2, dato3, dato4, dato5))
        db.commit()
        db.close()

    def insertar_cursosvacios(self, dato1, tabla):
        db=self.conectar()
        cur=db.cursor()
        cur.execute(u"""INSERT INTO """+ tabla +""" (curso) VALUES (%s)""" ,
            (dato1))
        db.commit()
        db.close()
        
    def insertar_datos_trip(self, s, p, o, tabla):
        db=self.conectar()
        cur=db.cursor()
        #print 'sujeto= %s'%s
        #print 'predicado= %s'%p
        #print 'objeto= %s'%o
        #o=str(o).decode('utf-8')
        #o=unicodedata.normalize('NFKD', o).encode('ascii','ignore')
        cur.execute(u"""INSERT INTO """+ tabla +""" (sujeto, predicado, objeto) VALUES (%s, %s, %s)""" ,
            (s, p, o))
        db.commit()
        db.close()
  

    def menus(self, urlcurso):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = " SELECT sujeto,predicado,objetolimpio as objeto FROM ScrapyMenu.triples_tripletes_2 where sujeto='%s' and predicado='menu';"%urlcurso
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    def recursomenus(self, urlmenu):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = " SELECT distinct sujeto,predicado,objetolimpio as objeto FROM ScrapyMenu.triples_tripletes_2 where sujeto='%s';"%urlmenu
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    def oersmenus(self, urlmenu):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT * FROM ScrapyMenu.enlaces_oers_union where sujeto='%s' or sujeto='%s/';"%(urlmenu,urlmenu)
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    def oersmenustitulo(self, urlmenu):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT * FROM ScrapyMenu.enlaces_oers_union where sujeto='%s';"%(urlmenu)
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    def infoers(self, urloers):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT * FROM ScrapyMenu.Metadatos_union_enlaces where enlace_oer='%s';"%urloers
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    def insertar_datos_CursoUrlSeparado(self,UrlUniversidad,UrlCompleta,tabla):
        db=self.conectar()
        cur=db.cursor()
        cur.execute(u"""INSERT INTO """+ tabla +""" (UrlUniversidad, UrlCompleta) VALUES (%s, %s)""" ,
            (UrlUniversidad, UrlCompleta))
        db.commit()
        db.close()


    def cursosmit(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.mit.edu%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    def cursosuc3(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.uc3m.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    def cursoslearnopen(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%openlearn.open.ac.uk%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    def cursosocwus(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocwus.us.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

        
    def CursosOcwUpmEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.upm.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    def CursosOcwUci(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.uci.edu%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    def CursosOcwAvuOrg(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%oer.avu.org%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    def CursosOcwUmEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.um.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    def CursosOcwUnicanEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.unican.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    def CursosOcwKoreaEdu(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.korea.edu%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    def CursosOcwUocEdu(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.uoc.edu%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    def CursosOcwJhsphEdu(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.jhsph.edu%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    
    def CursosOcwUvEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.uv.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwInnovaUnedEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.innova.uned.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    def CursosOcwUmbEdu(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.umb.edu%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwUdemEduMx(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.udem.edu.mx%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwUnizarEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.unizar.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwUsalEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.usal.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwOpenmarhiRu(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%www.open-marhi.ru%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwCursosUnavEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%www.unav.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    
    def CursosOcwUaEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.ua.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwHokudaiAcJp(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.hokudai.ac.jp%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwUctAcZa(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%opencontent.uct.ac.za%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwUmichEdu(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%open.umich.edu%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwUpvEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%www.upv.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwMetuEduTr(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.metu.edu.tr%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        CursosOcwTsukubaAcJp
    def CursosOcwTsukubaAcJp(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.tsukuba.ac.jp%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwNottinghamAcUk(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%unow.nottingham.ac.uk%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        

    def prueba(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT CursosMit.sujeto,CursosMit.predicado,CursosMit.objeto FROM ScrapyMenu.CursosMit,ScrapyMenu.CursosUrlSeparado where CursosMit.sujeto=CursosUrlSeparado.urlcompleta and CursosMit.predicado='link' limit 1000000000000;"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos