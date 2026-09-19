import tkinter
from ui.vista_personas import crear_vista_personas
from ui.vista_categorias import crear_vista_categorias
from ui.vista_gustos import crear_vista_gustos
from PIL import Image, ImageTk
import sys
import os

def ruta_base():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE = ruta_base()




ventana = tkinter.Tk()
ventana.geometry("900x600")
ventana.title("The Taste Vault")
ventana.configure(bg="#1C1917")

header = tkinter.Frame(ventana, bg="#151313", pady=20)
header.pack(side=tkinter.TOP, fill=tkinter.X)


img_logo = Image.open(os.path.join(BASE, "assets", "logo.png")).resize((40, 40))
img_logo_tk = ImageTk.PhotoImage(img_logo)

titulo = tkinter.Label(header, image=img_logo_tk, text="THE TASTE VAULT", compound=tkinter.LEFT,
                       bg="#151313", fg="#E8D5B7",
                       font=("Comic Sans MS", 18, "bold"), cursor="hand2")
titulo.image = img_logo_tk
titulo.pack()

menuBotones = tkinter.Frame(ventana, bg="#44403C", pady=10)
menuBotones.pack(fill=tkinter.X)

# ── CANVAS CENTRAL CON SCROLL ────────────────
scrollbar_y = tkinter.Scrollbar(ventana, orient=tkinter.VERTICAL)
scrollbar_x = tkinter.Scrollbar(ventana, orient=tkinter.HORIZONTAL)

canvas = tkinter.Canvas(ventana, bg="#1C1917", highlightthickness=0,
                        yscrollcommand=scrollbar_y.set,
                        xscrollcommand=scrollbar_x.set)

scrollbar_y.config(command=canvas.yview)
scrollbar_x.config(command=canvas.xview)

scrollbar_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)
scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)
canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

contenedor = tkinter.Frame(canvas, bg="#1C1917")
contenedor_window = canvas.create_window((0, 0), window=contenedor, anchor="nw")

def actualizar_scroll(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

contenedor.bind("<Configure>", actualizar_scroll)

def actualizar_ancho_contenedor(event=None):
    canvas.itemconfig(contenedor_window, width=event.width)
canvas.bind("<Configure>", actualizar_ancho_contenedor)

def _scroll_vertical(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") ##scroll de raton

def _scroll_horizontal(event):
    canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _scroll_vertical)
canvas.bind_all("<Shift-MouseWheel>", _scroll_horizontal)

# ── FRAMES DE VISTAS (dentro del contenedor) ─
frame_personas   = tkinter.Frame(contenedor, bg="#1C1917")
frame_categorias = tkinter.Frame(contenedor, bg="#1C1917")
frame_gustos     = tkinter.Frame(contenedor, bg="#1C1917")

def mostrar_personas():
    frame_categorias.pack_forget()
    frame_gustos.pack_forget()
    frame_personas.pack(fill=tkinter.BOTH, expand=True)
    crear_vista_personas(frame_personas, menuBotones, mostrar_categorias)

def mostrar_categorias(persona_id, persona_nombre):
    frame_personas.pack_forget()
    frame_gustos.pack_forget()
    frame_categorias.pack(fill=tkinter.BOTH, expand=True)
    crear_vista_categorias(frame_categorias, menuBotones, persona_id, persona_nombre, mostrar_personas, mostrar_gustos)

def mostrar_gustos(categoria_id, categoria_nombre, persona_id, persona_nombre):
    frame_personas.pack_forget()
    frame_categorias.pack_forget()
    frame_gustos.pack(fill=tkinter.BOTH, expand=True)
    crear_vista_gustos(frame_gustos, menuBotones, categoria_id, categoria_nombre, persona_id, persona_nombre, mostrar_categorias)

titulo.bind("<Button-1>", lambda e: mostrar_personas())