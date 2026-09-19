import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
from db.queries import crear_persona, editar_persona, eliminar_persona, obtener_personas

def crear_vista_personas(frame_personas, menuBotones, mostrar_categorias):

    for t in frame_personas.winfo_children():
        t.destroy()

    def borrar_menu():
        for t in menuBotones.winfo_children():
            t.destroy()

    body = tkinter.Frame(frame_personas, bg="#1C1917")
    body.pack(fill=tkinter.BOTH, expand=True)

    def construir_menu_principal():
        borrar_menu()
        tkinter.Button(menuBotones, text="CREAR PERSONA",
                       command=abrir_formulario_creacion_persona,
                       bg="#E8D5B7", fg="#1C1917",
                       relief=tkinter.FLAT, padx=10, pady=4,
                       font=("Arial", 9, "bold"),
                       activebackground="#D4B896", activeforeground="#1C1917"
                       ).pack(side=tkinter.LEFT, padx=5)
    
        tkinter.Label(menuBotones, text="PERSONAS",
                        bg="#292524", fg="#E8D5B7",
                          font=("Arial", 10, "bold")).pack()

    def cargar_tarjetas():
        for t in body.winfo_children():
            t.destroy()
        construir_menu_principal()

        personas = obtener_personas()
        numero_de_tarjeta = 0

        for persona in personas:
            persona_id     = persona[0]
            nombre_persona = persona[1]
            imagen_persona = persona[2]

            fila    = numero_de_tarjeta // 5
            columna = numero_de_tarjeta % 5

            tarjeta = tkinter.Frame(body, bg="#292524", padx=10, pady=10)
            tarjeta.grid(row=fila, column=columna, padx=5, pady=5)

            try:
                img = Image.open(imagen_persona).resize((250, 250))
            except:
                img = Image.new("RGB", (250, 250), color="#44403C")

            img_tk = ImageTk.PhotoImage(img)

            imagen = tkinter.Button(tarjeta, image=img_tk,
                                    command=lambda pid=persona_id, pn=nombre_persona: mostrar_categorias(pid, pn),
                                    bg="#292524", relief=tkinter.FLAT,
                                    activebackground="#44403C")
            imagen.image = img_tk
            imagen.pack()

            tkinter.Label(tarjeta, text=nombre_persona,
                          bg="#292524", fg="#E8D5B7",
                          font=("Arial", 10, "bold")).pack()

            frame_botones = tkinter.Frame(tarjeta, bg="#292524")
            frame_botones.pack()

            tkinter.Button(frame_botones, text="EDITAR",
                           bg="#44403C", fg="#E8D5B7",
                           relief=tkinter.FLAT, padx=8, pady=2,
                           activebackground="#57534E", activeforeground="#E8D5B7",
                           command=lambda pid=persona_id, pn=nombre_persona, pi=imagen_persona:
                           abrir_formulario_edicion_persona(pid, pn, pi)
                           ).pack(side=tkinter.LEFT, padx=2)

            tkinter.Button(frame_botones, text="BORRAR",
                           bg="#7C2D12", fg="#FEF3C7",
                           relief=tkinter.FLAT, padx=8, pady=2,
                           activebackground="#9A3412", activeforeground="#FEF3C7",
                           command=lambda pid=persona_id: borrar_persona(pid)
                           ).pack(side=tkinter.LEFT, padx=2)

            numero_de_tarjeta += 1

    def borrar_persona(persona_id):
        eliminar_persona(persona_id)
        cargar_tarjetas()

    def abrir_formulario_creacion_persona():
        for t in body.winfo_children():
            t.destroy()
        borrar_menu()

        tkinter.Label(menuBotones, text="CREAR PERSONA",
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
                       command=lambda: crear_persona_y_actualizar(nombre_input.get(), imagen_path["ruta"]),
                       bg="#E8D5B7", fg="#1C1917",
                       relief=tkinter.FLAT, padx=20, pady=8,
                       font=("Arial", 10, "bold"),
                       activebackground="#D4B896", activeforeground="#1C1917"
                       ).pack(pady=10)

    def crear_persona_y_actualizar(nombre_in, imagen_in):
        if nombre_in:
            crear_persona(nombre_in, imagen_in)
            cargar_tarjetas()

    def abrir_formulario_edicion_persona(persona_id, p_nombre, p_imagen):
        for t in body.winfo_children():
            t.destroy()
        borrar_menu()

        tkinter.Label(menuBotones, text="EDITAR PERSONA",
                      bg="#E8D5B7", fg="#1C1917",
                       relief=tkinter.FLAT, padx=10, pady=4,
                       font=("Arial", 9, "bold"),
                       activebackground="#D4B896", activeforeground="#1C1917"
                       ).pack(side=tkinter.LEFT, padx=10)
        tkinter.Button(menuBotones, text="VOLVER", command=cargar_tarjetas,
                       bg="#E8D5B7", fg="#1C1917",
                       relief=tkinter.FLAT, padx=10, pady=4,
                       font=("Arial", 9, "bold"),
                       activebackground="#D4B896", activeforeground="#1C1917"
                       ).pack(side=tkinter.RIGHT, padx=10)

        imagen_path = {"ruta": p_imagen}

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
        nombre_input.insert(0, p_nombre)
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
            img = Image.open(p_imagen).resize((250, 250))
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
                       command=lambda: editar_persona_y_actualizar(persona_id, nombre_input.get(), imagen_path["ruta"]),
                       bg="#E8D5B7", fg="#1C1917",
                       relief=tkinter.FLAT, padx=20, pady=8,
                       font=("Arial", 10, "bold"),
                       activebackground="#D4B896", activeforeground="#1C1917"
                       ).pack(pady=10)

    def editar_persona_y_actualizar(persona_id, nombre_in, imagen_in):
        if nombre_in:
            editar_persona(persona_id, nombre_in, imagen_in)
            cargar_tarjetas()

    cargar_tarjetas()