import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
from db.queries import crear_gusto, editar_gusto, eliminar_gusto, obtener_gustos


def crear_vista_gustos(frame_gustos, menuBotones, categoria_id, categoria_nombre, persona_id, persona_nombre, mostrar_categorias):
    
    
    # limpiar frame por si se reconstruye al volver
    for t in frame_gustos.winfo_children():
        t.destroy()

    def borrar_menu():
        for t in menuBotones.winfo_children():
            t.destroy()
    
    # ── BODY ─────────────────────────────────
    body = tkinter.Frame(frame_gustos, bg="#1C1917")
    body.pack(fill=tkinter.BOTH, expand=True)

    # ── MENÚ PRINCIPAL ────────────────────────
    def construir_menu_principal():
        borrar_menu()
        
        tkinter.Button(menuBotones, text="VOLVER",
               command=lambda: mostrar_categorias(persona_id, persona_nombre),
               bg="#E8D5B7", fg="#1C1917",
               relief=tkinter.FLAT, padx=10, pady=4,
               font=("Arial", 9, "bold"),
               activebackground="#D4B896", activeforeground="#1C1917"
               ).pack(side=tkinter.RIGHT, padx=10)
        
    
        tkinter.Label(menuBotones, text=f"GUSTOS DE LA CATEGORÍA:: {categoria_nombre}",
                        bg="#292524", fg="#E8D5B7",
                          font=("Arial", 10, "bold")).pack()

        tkinter.Button(menuBotones, text="CREAR GUSTO",
                       command=abrir_formulario_creacion_gusto,
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

        gustos = obtener_gustos(categoria_id)
        numero_de_tarjeta = 0

        for gusto in gustos:
            gusto_id     = gusto[0]
            nombre_gusto = gusto[1]
            imagen_gusto = gusto[2]
            interes_gusto = gusto[3]

            fila    = numero_de_tarjeta // 5
            columna = numero_de_tarjeta % 5

            tarjeta = tkinter.Frame(body, bg="#292524", padx=10, pady=10)
            tarjeta.grid(row=fila, column=columna, padx=5, pady=5)

            try:
                img = Image.open(imagen_gusto).resize((250, 250))
            except:
                img = Image.new("RGB", (250, 250), color="#44403C")

            img_tk = ImageTk.PhotoImage(img)

            imagen = tkinter.Button(tarjeta, image=img_tk,
                                    bg="#292524", relief=tkinter.FLAT,
                                    activebackground="#44403C")
            imagen.image = img_tk
            imagen.pack()

            tkinter.Label(tarjeta, text=nombre_gusto,
                          bg="#292524", fg="#E8D5B7",
                          font=("Arial", 10, "bold")).pack()
            tkinter.Label(tarjeta, text=f"Puntos de interés: {interes_gusto}",
              bg="#292524", fg="#A8A29E",
              font=("Arial", 9)).pack()

            frame_botones = tkinter.Frame(tarjeta, bg="#292524")
            frame_botones.pack()

            tkinter.Button(frame_botones, text="EDITAR",
                           bg="#44403C", fg="#E8D5B7",
                           relief=tkinter.FLAT, padx=8, pady=2,
                           activebackground="#57534E", activeforeground="#E8D5B7",
                           command=lambda gid=gusto_id, gn=nombre_gusto, gi_=interes_gusto, gi=imagen_gusto:
                           abrir_formulario_edicion_gusto(gid, gn, gi_, gi)
                           ).pack(side=tkinter.LEFT, padx=2)

            tkinter.Button(frame_botones, text="BORRAR",
                           bg="#7C2D12", fg="#FEF3C7",
                           relief=tkinter.FLAT, padx=8, pady=2,
                           activebackground="#9A3412", activeforeground="#FEF3C7",
                           command=lambda pid=gusto_id: borrar_gusto(pid)
                           ).pack(side=tkinter.LEFT, padx=2)

            numero_de_tarjeta += 1


    # ── BORRAR gusto ────────────────────────
    def borrar_gusto(gusto_id):
        eliminar_gusto(gusto_id)
        cargar_tarjetas()

    

    # ── FORMULARIO CREAR ─────────────────────
    def abrir_formulario_creacion_gusto():
        for t in body.winfo_children():
            t.destroy()
        
        borrar_menu()

        tkinter.Label(menuBotones, text="CREAR GUSTO",
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

        tkinter.Label(body, text="PUNTOS DE INTERÉS",
              bg="#1C1917", fg="#A8A29E",
              font=("Arial", 8, "bold")).pack(anchor=tkinter.W, padx=20, pady=(20, 0))
        puntos_var = tkinter.StringVar(value="1")
        puntos_input = tkinter.OptionMenu(body, puntos_var, "1", "2", "3")
        puntos_input.config(bg="#292524", fg="#E8D5B7", relief=tkinter.FLAT,
                    activebackground="#44403C", highlightthickness=0)
        puntos_input.pack(anchor=tkinter.W, padx=20)


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
                       command=lambda: crear_categoria_y_actualizar(puntos_var.get(), nombre_input.get(), imagen_path["ruta"]),
                       bg="#E8D5B7", fg="#1C1917",
                       relief=tkinter.FLAT, padx=20, pady=8,
                       font=("Arial", 10, "bold"),
                       activebackground="#D4B896", activeforeground="#1C1917"
                       ).pack(pady=10)

    # ── CREAR Y RECARGAR ──────────────────────
    def crear_categoria_y_actualizar(puntos_in, nombre_in, imagen_in):
        if nombre_in:
            crear_gusto(puntos_in, categoria_id, nombre_in, imagen_in)
            cargar_tarjetas()




    # ── FORMULARIO EDITAR ─────────────────────
    def abrir_formulario_edicion_gusto(gusto_id, g_nombre, g_interes, g_imagen):
        for t in body.winfo_children():
            t.destroy()
        borrar_menu()

        tkinter.Label(menuBotones, text="EDITAR GUSTOS",
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

        imagen_path = {"ruta": g_imagen}  # ruta actual de la imagen

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
        nombre_input.insert(0, g_nombre)
        nombre_input.pack(padx=20)

        
        tkinter.Label(body, text="PUNTOS DE INTERÉS",
              bg="#1C1917", fg="#A8A29E",
              font=("Arial", 8, "bold")).pack(anchor=tkinter.W, padx=20, pady=(20, 0))
        puntos_var = tkinter.StringVar(value=str(g_interes))
        puntos_input = tkinter.OptionMenu(body, puntos_var, "1", "2", "3")
        puntos_input.config(bg="#292524", fg="#E8D5B7", relief=tkinter.FLAT,
                    activebackground="#44403C", highlightthickness=0)
        puntos_input.pack(anchor=tkinter.W, padx=20)

        tkinter.Label(body, text="IMAGEN",
                      bg="#1C1917", fg="#A8A29E",
                      font=("Arial", 8, "bold")).pack(anchor=tkinter.W, padx=20, pady=(20, 0))

        frame_imagen = tkinter.Frame(body, bg="#292524", height=100)
        frame_imagen.pack(fill=tkinter.X, padx=20)
        frame_imagen.pack_propagate(False)

        preview = tkinter.Label(frame_imagen, bg="#292524")
        preview.pack(side=tkinter.LEFT, padx=10)

        try:
            img = Image.open(g_imagen).resize((250, 250))
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
               command=lambda: editar_gusto_y_actualizar(gusto_id, nombre_input.get(), puntos_var.get(), imagen_path["ruta"])
               ).pack(pady=10)



    # ── EDITAR Y RECARGAR ─────────────────────
    def editar_gusto_y_actualizar(gusto_id, nombre_in, puntos_in, imagen_in):
        if nombre_in:
            editar_gusto(gusto_id, nombre_in, puntos_in, categoria_id, imagen_in)
            cargar_tarjetas()



     # arrancar
    cargar_tarjetas()