# -*- coding: utf-8-sig -*-
import codecs
import MySQLdb
#from config import *
import MySQLdb as mdb
import unicodedata

HOSTLord=''
USERLord=''
PASSLord=''
BDLord=''
HOST=''    
USER=''
PASS=''
BD=''
class BDdatos():
    def configuracionLord(self,host,user,clave,bd):
        global HOSTLord
        global USERLord
        global PASSLord
        global BDLord

        HOSTLord=host
        USERLord=user
        PASSLord=clave
        BDLord=bd
    def configuracion(self,host,user,clave,bd):
        global HOST
        global USER
        global PASS
        global BD
        HOST=host
        USER=user
        PASS=clave
        BD=bd
    """
        Clase para la Base de Datos
    """
    def conectar(self):
        global HOST
        global USER
        global PASS
        global BD
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
    def conectarlord(self):
        global HOSTLord
        global USERLord
        global PASSLord
        global BDLord
        """
           conectarme a la bd
        """
        db = None
        try:
            #obtener datos de autentificacion de la base de datos
            host = HOSTLord
            user = USERLord
            clave = PASSLord
            base_datos = BDLord
            db=MySQLdb.connect(host=host,user=user,passwd=clave,db=base_datos,charset='utf8',use_unicode=True )
        except Exception, e:
            print "error de coneccion", e
        return db
    
    def cerrar(self, db):
        """
            cerrar la base de datos
        """
        db.close()

    def insertar_datos_trip_Tabla(self,tabla1,tabala2):
        db=self.conectar()
        cur=db.cursor()
        sql="INSERT INTO %s SELECT * FROM %s"%(tabla1,tabala2)
        cur.execute(sql)
        db.commit()
        db.close()

    def CursosConsortium(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.ConsortiumCursos where predicado='urlCourseOCWC';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    def CursosConsortiumFaltantes(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT sujeto FROM ScrapyMenu.CursosConsortiumFaltantes3;"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    def consulta(self, consulta):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = consulta
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

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

    def crearTabla(self,nombretabla):
        db=self.conectar()
        cur=db.cursor()
        cur.execute(u"""CREATE  TABLE ScrapyMenu."""+ nombretabla +"""( sujeto TEXT CHARACTER SET 'utf8' NULL , predicado TEXT CHARACTER SET 'utf8' NULL , objeto LONGTEXT CHARACTER SET 'utf8' NULL ) DEFAULT CHARACTER SET = utf8;""")
        db.commit()
        db.close()
    def crearTablalord(self,nombretabla):
        db=self.conectarlord()
        cur=db.cursor()
        cur.execute(u"""CREATE  TABLE """+ nombretabla +"""( sujeto TEXT CHARACTER SET 'utf8' NULL , predicado TEXT CHARACTER SET 'utf8' NULL , objeto LONGTEXT CHARACTER SET 'utf8' NULL ) DEFAULT CHARACTER SET = utf8;""")
        db.commit()
        db.close()

        
    def insertar_datos_trip(self, s, p, o, tabla):
        db=self.conectar()
        cur=db.cursor()
        cur.execute(u"""INSERT INTO """+ tabla +""" (sujeto, predicado, objeto) VALUES (%s, %s, %s)""" ,
            (s, p, o))
        db.commit()
        db.close()
    #def insertar_datos_trip(self, s, p, o,sp,op, tabla):
    #    db=self.conectarlord()
    #    cur=db.cursor()
    #    cur.execute(u"""INSERT INTO """+ tabla +""" (sujeto, predicado, objeto,sujetoper,objetoper) VALUES (%s, %s, %s,%s,%s)""" ,
    #        (s, p, o,sp,op))
    #    db.commit()
    #    db.close()
    def insertar_datos_trip_lord(self, s, p, o, tabla):
        db=self.conectarlord()
        cur=db.cursor()
        cur.execute(u"""INSERT INTO """+ tabla +""" (sujeto, predicado, objeto) VALUES (%s, %s, %s)""" ,
            (s, p, o))
        db.commit() 
        db.close()
    def insertar_datos_trip_per_lord(self, s, p, o,sp,op, tabla):
        db=self.conectarlord()
        cur=db.cursor()
        cur.execute(u"""INSERT INTO """+ tabla +""" (sujeto, predicado, objeto,sujetoper,objetoper) VALUES (%s, %s, %s,%s,%s)""" ,
            (s, p, o,sp,op))
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

    def ConsortiumMienmbros(self):
        db=self.conectar() 
        cursor=db.cursor()
        sql = "select * from ConsortiumMienmbros where predicado='titulo' limit 240000000000;"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

