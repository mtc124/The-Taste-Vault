import sqlite3
import os
import sqlite3
import sys


def ruta_base():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(ruta_base(), "gustos.db")

def obtener_personas():
    conection= sqlite3.connect(DB_PATH)
    cursor= conection.cursor()
    cursor.execute(
        "SELECT * FROM personas"
    )
    personas = cursor.fetchall() ##captura resultados para devolverlos
    conection.close()
    return personas


def crear_persona(nombre, imagen=None):
    conection=sqlite3.connect(DB_PATH)
    cursor=conection.cursor()
    cursor.execute(
        "INSERT INTO personas(nombre, imagen) VALUES ( ?, ?)" , (nombre, imagen)
    )
    conection.commit()
    conection.close()



def editar_persona(id, nombre, imagen=None):
    conection=sqlite3.connect(DB_PATH)
    cursor=conection.cursor()
    cursor.execute(
        "UPDATE personas SET nombre=?, imagen=? WHERE id=?", (nombre, imagen, id)
    )
    conection.commit()
    conection.close()
    


def eliminar_persona(id):
    conection=sqlite3.connect(DB_PATH)
    cursor=conection.cursor()
    cursor.execute(
        "DELETE FROM  personas WHERE id = ?", (id,)
    )
    conection.commit()
    conection.close()
    
    

def obtener_categorias(persona_id):
    conection= sqlite3.connect(DB_PATH)
    cursor= conection.cursor()
    cursor.execute(
        "SELECT * FROM categorias WHERE persona_id=? ", (persona_id,)
    )
    categorias = cursor.fetchall()
    conection.close()
    return categorias


def crear_categoria(nombre, persona_id, imagen=None):
    conection=sqlite3.connect(DB_PATH)
    cursor=conection.cursor()
    cursor.execute(
        "INSERT INTO categorias(nombre, imagen, persona_id) VALUES(?, ?, ?)", (nombre, imagen, persona_id)
    )
    conection.commit()
    conection.close()
    


def editar_categoria(id, nombre, persona_id, imagen=None):
    conection=sqlite3.connect(DB_PATH)
    cursor=conection.cursor()
    cursor.execute(
        "UPDATE categorias SET nombre=?, imagen=?, persona_id=? WHERE id=?", (nombre, imagen, persona_id, id)
    )
    conection.commit()
    conection.close()
    


def eliminar_categoria(id):
    conection=sqlite3.connect(DB_PATH)
    cursor=conection.cursor()
    cursor.execute(
        "DELETE FROM categorias WHERE id=?", (id,)
    )
    conection.commit()
    conection.close()
    


def obtener_gustos(categoria_id):
    conection= sqlite3.connect(DB_PATH)
    cursor= conection.cursor()
    cursor.execute(
        "SELECT * FROM gustos WHERE categoria_id = ?", (categoria_id,)
    )
    gustos= cursor.fetchall()
    conection.close()
    return gustos



def crear_gusto(puntos_interes, categoria_id, nombre=None, imagen=None):
    conection=sqlite3.connect(DB_PATH)
    cursor=conection.cursor()
    cursor.execute(
        "INSERT INTO gustos(nombre, imagen, puntos_interes, categoria_id) VALUES (?, ?, ?, ?)", (nombre, imagen, int(puntos_interes), categoria_id)
    )
    conection.commit()
    conection.close()
    


def editar_gusto(id, nombre, puntos_interes, categoria_id, imagen=None):
    conection=sqlite3.connect(DB_PATH)
    cursor=conection.cursor()
    cursor.execute(
        "UPDATE gustos SET nombre=?, imagen=?, puntos_interes=?, categoria_id=? WHERE id=?", (nombre, imagen, int(puntos_interes), categoria_id, id)
    )
    conection.commit()
    conection.close()
    


def eliminar_gusto(id):
    conection=sqlite3.connect(DB_PATH)
    cursor=conection.cursor()
    cursor.execute(
        "DELETE FROM gustos where id=?", (id,)
    )
    conection.commit()
    conection.close()
    

