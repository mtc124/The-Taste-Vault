import sqlite3
import os

import sys
import os

def ruta_base():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)  
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE = ruta_base()
DB_PATH = os.path.join(BASE, "gustos.db")


def crear_tablas():
        conection = sqlite3.connect(DB_PATH) ##conexion con gustos.db
        cursor=conection.cursor() ##ejecuta queries

        ##ejecuta codigo sql
        cursor.executescript("""CREATE TABLE IF NOT EXISTS personas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                imagen TEXT
        
        );

         CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL, 
                imagen TEXT,
                persona_id INTEGER NOT NULL,
                FOREIGN KEY (persona_id) REFERENCES personas(id)

        );

         CREATE TABLE IF NOT EXISTS gustos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL, 
                imagen TEXT,
                puntos_interes INTEGER NOT NULL CHECK (puntos_interes>=1 AND puntos_interes<=3),
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)

        );""")

        conection.commit() ##guarda los cambios (las tablas que ha creado el cursor)
        conection.close() ##cierra conexion
        print("tablas creadas")

if __name__ == "__main__":
    crear_tablas()
                