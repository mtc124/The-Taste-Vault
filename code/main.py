from db.database import crear_tablas
crear_tablas()

from ui.app import ventana, mostrar_personas

if __name__ == "__main__":
    mostrar_personas()
    ventana.mainloop()