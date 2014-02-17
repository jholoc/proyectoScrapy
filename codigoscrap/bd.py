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
    def conectarlord(self):
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
    
    def CursosOcwAghEduPl(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%open.agh.edu.pl%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwNckuEduTw(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%yct.ncku.edu.tw%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        cursosOcwNdEdu
    def cursosOcwNdEdu(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.nd.edu%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def cursosTuftsEdu(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.tufts.edu%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwUtmMy(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.utm.my%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def cursosUnioviEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.uniovi.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def cursosUdlCat(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.udl.cat%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def cursosTmuEduTw(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.tmu.edu.tw:8080%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwNjitEdu(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.njit.edu%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def cursosTudelftNl(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.tudelft.nl%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwUgrEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.ugr.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwUnuEdu(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.unu.edu%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwUibEs(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.uib.es%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    
    def CursosOcwUabCat(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.uab.cat%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwUnedAcCr(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.uned.ac.cr%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwUtplEduEc(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.utpl.edu.ec%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwSbuAcIr(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.sbu.ac.ir%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos

    def CursosOcwUsuAcId(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.usu.ac.id%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        UnivalleEduCo
    def CursosOcwUnivalleEduCo(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.univalle.edu.co%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwIcesiEduCo(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%www.icesi.edu.co%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwKyushuuAcJp(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%ocw.kyushu-u.ac.jp%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        
    def CursosOcwMetropoliaFi(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.OCWC_cursos where objeto like '%wiki.metropolia.fi%';"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    
    def CursosOcwUniversia(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct sujeto FROM ScrapyMenu.universia_cursos;"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
    def CursosUniversia(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.CursosUniversia where predicado='link' limit 1000000000000000;"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.close()
        return datos
        CursosOcwVideoLectures
    def CursosOcwVideoLectures(self):
        """
            conectarme a la bd, para sacar los datos necesarios
        """
        db=self.conectar() 
        cursor=db.cursor()
        sql = "SELECT distinct objeto FROM ScrapyMenu.VideoLectures;"
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