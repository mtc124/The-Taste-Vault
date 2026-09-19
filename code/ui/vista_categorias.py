import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
from db.queries import crear_categoria, editar_categoria, eliminar_categoria, obtener_categorias



def crear_vista_categorias(frame_categorias, menuBotones, persona_id, persona_nombre, mostrar_personas, mostrar_gustos):
     
    
    # limpiar frame por si se reconstruye al volver
    for t in frame_categorias.winfo_children():
        t.destroy()

    def borrar_menu():
        for t in menuBotones.winfo_children():
            t.destroy()
    borrar_menu()
    # ── BODY ─────────────────────────────────
    body = tkinter.Frame(frame_categorias, bg="#1C1917")
    body.pack(fill=tkinter.BOTH, expand=True)

    # ── MENÚ PRINCIPAL ────────────────────────
    def construir_menu_principal():
        borrar_menu()
        tkinter.Button(menuBotones, text="VOLVER",
                       command=mostrar_personas,
                       bg="#E8D5B7", fg="#1C1917",
                       relief=tkinter.FLAT, padx=10, pady=4,
                       font=("Arial", 9, "bold"),
                       activebackground="#D4B896", activeforeground="#1C1917"
                       ).pack(side=tkinter.RIGHT, padx=5)
        
    
        tkinter.Label(menuBotones, text=f"CATEGORÍAS DE: {persona_nombre}",
                        bg="#292524", fg="#E8D5B7",
                          font=("Arial", 10, "bold")).pack()

        tkinter.Button(menuBotones, text="CREAR CATEGORIA",
                       command=abrir_formulario_creacion_categoria,
                       bg="#E8D5B7", fg="#1C1917",
                       relief=tkinter.FLAT, padx=10, pady=4,
                       font=("Arial", 9, "bold"),
                       activebackground="#D4B896", activeforeground="#1C1917"
                       ).pack(side=tkinter.LEFT, padx=5)


    # ── CARGAR TARJETAS ───────────────────────
    def cargar_tarjetas():
        for t in body.winfo_children():
            t.destroy()
        construir_menu_principal()

        categorias = obtener_categorias(persona_id)
        numero_de_tarjeta = 0

        for categoria in categorias:
            categoria_id     = categoria[0]
            nombre_categoria = categoria[1]
            imagen_categoria = categoria[2]

            fila    = numero_de_tarjeta // 5
            columna = numero_de_tarjeta % 5

            tarjeta = tkinter.Frame(body, bg="#292524", padx=10, pady=10)
            tarjeta.grid(row=fila, column=columna, padx=5, pady=5)

            try:
                img = Image.open(imagen_categoria).resize((250, 250))
            except:
                img = Image.new("RGB", (250, 250), color="#44403C")

            img_tk = ImageTk.PhotoImage(img)

            imagen = tkinter.Button(tarjeta, image=img_tk,
                        command=lambda pid=categoria_id, pn=nombre_categoria: mostrar_gustos(pid, pn, persona_id, persona_nombre),
                        bg="#292524", relief=tkinter.FLAT,
                        activebackground="#44403C")
            
            imagen.image = img_tk
            imagen.pack()

            tkinter.Label(tarjeta, text=nombre_categoria,
                          bg="#292524", fg="#E8D5B7",
                          font=("Arial", 10, "bold")).pack()

            frame_botones = tkinter.Frame(tarjeta, bg="#292524")
            frame_botones.pack()

            tkinter.Button(frame_botones, text="EDITAR",
                           bg="#44403C", fg="#E8D5B7",
                           relief=tkinter.FLAT, padx=8, pady=2,
                           activebackground="#57534E", activeforeground="#E8D5B7",
                           command=lambda cid=categoria_id, cn=nombre_categoria, ci=imagen_categoria:
                           abrir_formulario_edicion_categoria(cid, cn, ci)
                           ).pack(side=tkinter.LEFT, padx=2)

            tkinter.Button(frame_botones, text="BORRAR",
                           bg="#7C2D12", fg="#FEF3C7",
                           relief=tkinter.FLAT, padx=8, pady=2,
                           activebackground="#9A3412", activeforeground="#FEF3C7",
                           command=lambda cid=categoria_id: borrar_categoria(cid)
                           ).pack(side=tkinter.LEFT, padx=2)

            numero_de_tarjeta += 1


    # ── BORRAR categoria ────────────────────────
    def borrar_categoria(categoria_id):
        eliminar_categoria(categoria_id)
        cargar_tarjetas()

    
     # ── FORMULARIO CREAR ─────────────────────
    def abrir_formulario_creacion_categoria():
        for t in body.winfo_children():
            t.destroy()
        
        borrar_menu()

        tkinter.Label(menuBotones, text="CREAR CATEGORIA",
                      bg="#44403C", fg="#E8D5B7",
                      font=("Arial", 9, "bold")).pack(side=tkinter.LEFT, padx=10)
        tkinter.Button(menuBotones, text="VOLVER", command=cargar_tarjetas,
                       bg="#E8D5B7", fg="#1C1917",
                       relief=tkinter.FLAT, padx=10, pady=4,
                       font=("Arial", 9, "bold"),
                       activebackground="#D4B896", activeforeground="#1C1917"
                       ).pack(side=tkinter.RIGHT, padx=10)

        imagen_path = {"ruta": None}

        tkinter.Label(body, text="NOMBRE",
                      bg="#1C1917", fg="#A8A29E",
                      font=("Arial", 8, "bold")).pack(anchor=tkinter.W, padx=20, pady=(20, 0))
        nombre_input = tkinter.Entry(body, width=50,
                                     bg="#292524", fg="#E8D5B7",
                                     insertbackground="#E8D5B7",
                                     relief=tkinter.FLAT,
                                     highlightthickness=1,
                                     highlightbackground="#57534E",
                                     highlightcolor="#E8D5B7")
        nombre_input.pack(padx=20)

        tkinter.Label(body, text="IMAGEN",
                      bg="#1C1917", fg="#A8A29E",
                      font=("Arial", 8, "bold")).pack(anchor=tkinter.W, padx=20, pady=(20, 0))

        frame_imagen = tkinter.Frame(body, bg="#292524", height=100)
        frame_imagen.pack(fill=tkinter.X, padx=20)
        frame_imagen.pack_propagate(False)

        preview = tkinter.Label(frame_imagen, bg="#292524", text="Sin imagen",
                                fg="#78716C")
        preview.pack(side=tkinter.LEFT, padx=10)

        def seleccionar_imagen():
            ruta = filedialog.askopenfilename(
                filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif")]
            )
            if ruta:
                imagen_path["ruta"] = ruta
                img = Image.open(ruta).resize((80, 80))
                img_tk = ImageTk.PhotoImage(img)
                preview.config(image=img_tk, text="")
                preview.image = img_tk

        tkinter.Button(frame_imagen, text="SUBIR IMAGEN",
                       command=seleccionar_imagen,
                       bg="#44403C", fg="#E8D5B7",
                       relief=tkinter.FLAT, padx=10, pady=4,
                       activebackground="#57534E", activeforeground="#E8D5B7"
                       ).pack(side=tkinter.RIGHT, padx=10)

        tkinter.Button(body, text="CONFIRMAR",
                       command=lambda: crear_categoria_y_actualizar(nombre_input.get(), imagen_path["ruta"]),
                       bg="#E8D5B7", fg="#1C1917",
                       relief=tkinter.FLAT, padx=20, pady=8,
                       font=("Arial", 10, "bold"),
                       activebackground="#D4B896", activeforeground="#1C1917"
                       ).pack(pady=10)

    # ── CREAR Y RECARGAR ──────────────────────
    def crear_categoria_y_actualizar(nombre_in, imagen_in):
        if nombre_in:
            crear_categoria(nombre_in, persona_id, imagen_in)
            cargar_tarjetas()



    # ── FORMULARIO EDITAR ─────────────────────
    def abrir_formulario_edicion_categoria(categoria_id, c_nombre, c_imagen):
        for t in body.winfo_children():
            t.destroy()
        borrar_menu()

        tkinter.Label(menuBotones, text="EDITAR CATEGORIA",
                      bg="#E8D5B7", fg="#1C1917",
                      relief=tkinter.FLAT, padx=10, pady=4,
                      font=("Arial", 9, "bold"),
                      ).pack(side=tkinter.LEFT, padx=10)
        tkinter.Button(menuBotones, text="VOLVER", command=cargar_tarjetas,
                       bg="#E8D5B7", fg="#1C1917",
                       relief=tkinter.FLAT, padx=10, pady=4,
                       font=("Arial", 9, "bold"),
                       activebackground="#D4B896", activeforeground="#1C1917"
                       ).pack(side=tkinter.RIGHT, padx=10)

        imagen_path = {"ruta": c_imagen}  # ruta actual de la imagen

        tkinter.Label(body, text="NOMBRE",
                      bg="#1C1917", fg="#A8A29E",
                      font=("Arial", 8, "bold")).pack(anchor=tkinter.W, padx=20, pady=(20, 0))
        nombre_input = tkinter.Entry(body, width=50,
                                     bg="#292524", fg="#E8D5B7",
                                     insertbackground="#E8D5B7",
                                     relief=tkinter.FLAT,
                                     highlightthickness=1,
                                     highlightbackground="#57534E",
                                     highlightcolor="#E8D5B7")
        nombre_input.insert(0, c_nombre)
        nombre_input.pack(padx=20)

        tkinter.Label(body, text="IMAGEN",
                      bg="#1C1917", fg="#A8A29E",
                      font=("Arial", 8, "bold")).pack(anchor=tkinter.W, padx=20, pady=(20, 0))

        frame_imagen = tkinter.Frame(body, bg="#292524", height=100)
        frame_imagen.pack(fill=tkinter.X, padx=20)
        frame_imagen.pack_propagate(False)

        preview = tkinter.Label(frame_imagen, bg="#292524")
        preview.pack(side=tkinter.LEFT, padx=10)

        try:
            img = Image.open(c_imagen).resize((250, 250))
            img_tk = ImageTk.PhotoImage(img)
            preview.config(image=img_tk)
            preview.image = img_tk
        except:
            preview.config(text="Sin imagen", fg="#78716C")

        def seleccionar_imagen():
            ruta = filedialog.askopenfilename(
                filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif")]
            )
            if ruta:
                imagen_path["ruta"] = ruta
                img = Image.open(ruta).resize((80, 80))
                img_tk = ImageTk.PhotoImage(img)
                preview.config(image=img_tk, text="")
                preview.image = img_tk

        tkinter.Button(frame_imagen, text="SUBIR IMAGEN",
                       command=seleccionar_imagen,
                       bg="#44403C", fg="#E8D5B7",
                       relief=tkinter.FLAT, padx=10, pady=4,
                       activebackground="#57534E", activeforeground="#E8D5B7"
                       ).pack(side=tkinter.RIGHT, padx=10)

        tkinter.Button(body, text="CONFIRMAR",
                       command=lambda: editar_categoria_y_actualizar(categoria_id, nombre_input.get(), imagen_path["ruta"]),
                       bg="#E8D5B7", fg="#1C1917",
                       relief=tkinter.FLAT, padx=20, pady=8,
                       font=("Arial", 10, "bold"),
                       activebackground="#D4B896", activeforeground="#1C1917"
                       ).pack(pady=10)


    # ── EDITAR Y RECARGAR ─────────────────────
    def editar_categoria_y_actualizar(categoria_id, nombre_in, imagen_in):
        if nombre_in: 
            editar_categoria(categoria_id, nombre_in, persona_id, imagen_in)
            cargar_tarjetas()



    # arrancar
    cargar_tarjetas()