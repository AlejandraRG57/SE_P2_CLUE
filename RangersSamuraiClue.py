import random
import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

# Función para obtener el path de los recursos empaquetados
def resource_path(relative_path):
    """ Devuelve la ruta absoluta del archivo, considerando si estamos empaquetados con PyInstaller. """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Listas de personajes, armas y locaciones originales
personajes_originales = ["Ranger Rojo", "Ranger Azul", "Ranger Rosa", "Ranger Verde", "Ranger Amarilla"]
armas_originales = ["Lanza fuego", "Hidro arco", "Aero abanico", "Lanza forestal", "Hoja terrestre"]
locaciones_originales = ["Dojo", "Patio", "Sala", "Mega Zord", "Muelle"]

# Hacer copias para manipular
personajes = personajes_originales.copy()
armas = armas_originales.copy()
locaciones = locaciones_originales.copy()

# Selección aleatoria de culpable, arma y locación
culpable = random.choice(personajes)
arma_misteriosa = random.choice(armas)
locacion_misteriosa = random.choice(locaciones)

# Eliminar las opciones seleccionadas de las listas para distribuir correctamente las pistas
personajes.remove(culpable)
armas.remove(arma_misteriosa)
locaciones.remove(locacion_misteriosa)

# Distribuir las armas y personajes restantes en las locaciones restantes
random.shuffle(personajes)
random.shuffle(armas)
random.shuffle(locaciones)

distribucion = {locaciones[i]: {"personajes": personajes[i], "armas": armas[i]} for i in range(len(locaciones))}

# Contador de preguntas
preguntas_restantes = 5

# Función para mostrar las reglas del juego
def mostrar_reglas():
    ventana_reglas = tk.Toplevel(root)
    ventana_reglas.title("Reglas del Juego")
    ventana_reglas.geometry("500x300")
    imagen2 = Image.open(resource_path("imagenes/Barco_Nightlock.jpg"))
    imagen2 = imagen2.resize((500, 300))  # Redimensionar según sea necesario
    fondo_tk2 = ImageTk.PhotoImage(imagen2)
    # Crear un label para mostrar la imagen de fondo
    label_fondo2 = tk.Label(ventana_reglas, image=fondo_tk2)
    label_fondo2.place(x=0, y=0, relwidth=1, relheight=1)  # Ajustar el fondo para cubrir toda la ventana
    reglas = """- Tienes 5 intentos para resolver el misterio.
    - En cada turno, puedes preguntar por un personaje, arma o locación.
    - Se te dará una pista basada en tu elección.
    - Al final, deberás adivinar quién es el culpable, con qué arma y en qué lugar ocurrió.
    ¡Buena suerte!"""
    tk.Label(ventana_reglas, text=reglas, padx=10, pady=10).pack()
    tk.Button(ventana_reglas, text="Cerrar", command=ventana_reglas.destroy).pack(pady=10)

    ventana_reglas.fondo_tk2 = fondo_tk2

# Función para mostrar la pista y la imagen en una ventana nueva
def mostrar_pista(pista, imagen_path=None):
    ventana_pista = tk.Toplevel(root)  # Nueva ventana para la pista
    ventana_pista.title("Pista")
    tk.Label(ventana_pista, text=pista, wraplength=250, padx=20, pady=20).pack()

    # Cargar y mostrar la imagen si se proporciona un camino
    if imagen_path:
        imagen = Image.open(resource_path(imagen_path))
        imagen = imagen.resize((300, 200))  # Redimensionar según sea necesario
        imagen_tk = ImageTk.PhotoImage(imagen)
        tk.Label(ventana_pista, image=imagen_tk).pack(pady=10)
        ventana_pista.image = imagen_tk  # Guardar una referencia

# Función para abrir la ventana de opciones de selección
def abrir_opciones(tipo_pregunta, opciones):
    opciones_ventana = tk.Toplevel(root)
    opciones_ventana.title(f"Seleccionar {tipo_pregunta}")

 #Zord_Toro
    opciones_ventana.geometry("500x300")
    imagen3 = Image.open(resource_path("imagenes/Zord_Toro.jpg"))
    imagen3 = imagen3.resize((500, 300))  # Redimensionar según sea necesario
    fondo_tk3 = ImageTk.PhotoImage(imagen3)
    # Crear un label para mostrar la imagen de fondo
    label_fondo3 = tk.Label(opciones_ventana, image=fondo_tk3)
    label_fondo3.place(x=0, y=0, relwidth=1, relheight=1)  # Ajustar el fondo para cubrir toda la ventana
    tk.Label(opciones_ventana, text=f"Elige un {tipo_pregunta}:", padx=20, pady=20).pack()
    opciones_ventana.fondo_tk3 = fondo_tk3

    for opcion in opciones:
        boton_opcion = tk.Button(opciones_ventana, text=opcion, command=lambda o=opcion: [opciones_ventana.withdraw(), dar_pistas(tipo_pregunta, o)])
        boton_opcion.pack(padx=10, pady=5)


# Función para manejar la selección de pistas
def dar_pistas(tipo_pregunta, respuesta):
    global preguntas_restantes

    pista_texto = ""
    pistas_dadas = False
    imagen_path = None  # Ruta de la imagen correspondiente

    for loc, datos in distribucion.items():
        personaje = datos["personajes"]
        arma = datos["armas"]

        if tipo_pregunta == "personajes" and respuesta == personaje:
            pista_texto = f"{personaje} fue visto en el {loc} con el arma {arma}."
            imagen_path = f"imagenes/{personaje.lower().replace(' ', '_')}.jpg"  # Ruta de la imagen del personaje
            pistas_dadas = True

        elif tipo_pregunta == "locaciones" and respuesta == loc:
            pista_texto = f"En {loc}, {personaje} estaba usando el arma {arma}."
            imagen_path = f"imagenes/{loc.lower().replace(' ', '_')}.jpg"  # Ruta de la imagen de la locación
            pistas_dadas = True

        elif tipo_pregunta == "armas" and respuesta == arma:
            pista_texto = f"El arma {arma} fue vista en el {loc} con {personaje}."
            imagen_path = f"imagenes/{arma.lower().replace(' ', '_')}.jpg"  # Ruta de la imagen del arma
            pistas_dadas = True

    if not pistas_dadas:
        pista_texto = "Tu elección no está relacionada con ninguna pista directa. Sigue buscando."
        imagen_path = None  # Sin imagen si no hay pistas

    mostrar_pista(pista_texto, imagen_path)

    # Reducir el número de preguntas restantes
    preguntas_restantes -= 1
    if preguntas_restantes == 0:
        root.withdraw()
        abrir_ventana_respuesta_final()  # Abrir ventana para la respuesta final
        

# Función para abrir la ventana de respuesta final
def abrir_ventana_respuesta_final():
    respuesta_ventana = tk.Toplevel()
    respuesta_ventana.title("Adivina el culpable")
    respuesta_ventana.geometry("500x800")
    #Mega_Zord_Full
    imagen4 = Image.open(resource_path("imagenes/Mega_Zord_Full.jpg"))
    imagen4 = imagen4.resize((500, 800))  # Redimensionar según sea necesario
    fondo_tk4 = ImageTk.PhotoImage(imagen4)
    # Crear un label para mostrar la imagen de fondo
    label_fondo4 = tk.Label(respuesta_ventana, image=fondo_tk4)
    label_fondo4.place(x=0, y=0, relwidth=1, relheight=1)  # Ajustar el fondo para cubrir toda la ventana
    respuesta_ventana.fondo_tk4 = fondo_tk4

    tk.Label(respuesta_ventana, text="Elige quién es el culpable:", padx=20, pady=10).pack()
    for personaje in personajes_originales:
        boton_personaje = tk.Button(respuesta_ventana, text=personaje, command=lambda p=personaje: seleccionar_respuesta("personaje", p, respuesta_ventana))
        boton_personaje.pack(padx=10, pady=5)

    tk.Label(respuesta_ventana, text="Elige el arma utilizada:", padx=20, pady=10).pack()
    for arma in armas_originales:
        boton_arma = tk.Button(respuesta_ventana, text=arma, command=lambda a=arma: seleccionar_respuesta("arma", a, respuesta_ventana))
        boton_arma.pack(padx=10, pady=5)

    tk.Label(respuesta_ventana, text="Elige la locación:", padx=20, pady=10).pack()
    for locacion in locaciones_originales:
        boton_locacion = tk.Button(respuesta_ventana, text=locacion, command=lambda l=locacion: seleccionar_respuesta("locacion", l, respuesta_ventana))
        boton_locacion.pack(padx=10, pady=5)

    # Variables para almacenar las respuestas seleccionadas
    respuesta_ventana.personaje_seleccionado = None
    respuesta_ventana.arma_seleccionada = None
    respuesta_ventana.locacion_seleccionada = None

# Función para manejar la selección final y mostrar la ventana de victoria o derrota
def seleccionar_respuesta(tipo, seleccion, ventana):
    if tipo == "personaje":
        ventana.personaje_seleccionado = seleccion
    elif tipo == "arma":
        ventana.arma_seleccionada = seleccion
    elif tipo == "locacion":
        ventana.locacion_seleccionada = seleccion

    # Verificar si ya se han seleccionado las tres opciones
    if ventana.personaje_seleccionado and ventana.arma_seleccionada and ventana.locacion_seleccionada:
        verificar_respuesta(ventana)

# Función para verificar la respuesta final y mostrar el resultado
def verificar_respuesta(ventana):
    if (ventana.personaje_seleccionado == culpable and
        ventana.arma_seleccionada == arma_misteriosa and
        ventana.locacion_seleccionada == locacion_misteriosa):
        mostrar_resultado("¡Felicidades! Has resuelto el misterio. Ganaste.", "Victoria", "victoria")
    else:
        mostrar_resultado(f"Lo siento, tu respuesta no es correcta.\nEra {culpable} con {arma_misteriosa} en {locacion_misteriosa}.", "Derrota", "derrota")
    ventana.destroy()



# Función para mostrar el resultado final en una nueva ventana
def mostrar_resultado(mensaje, titulo, imagen7):
    
    resultado_ventana = tk.Toplevel()
    resultado_ventana.title(titulo)
    resultado_ventana.geometry("500x300")
    imagen_path2 = f"imagenes/{imagen7.lower()}.jpg"
    Folderimage = Image.open(resource_path(imagen_path2))
    Folderimage =  Folderimage.resize((500, 300))  # Redimensionar según sea necesario
    fondo_tk7 = ImageTk.PhotoImage(Folderimage)
    # Crear un label para mostrar la imagen de fondo
    label_fondo7 = tk.Label(resultado_ventana, image=fondo_tk7)
    label_fondo7.place(x=0, y=0, relwidth=1, relheight=1)  # Ajustar el fondo para cubrir toda la ventana
    resultado_ventana.fondo_tk4 = fondo_tk7
    tk.Label(resultado_ventana, text=mensaje, padx=20, pady=20).pack()
    tk.Button(resultado_ventana, text="Cerrar", command=root.quit).pack(pady=10)
    resultado_ventana.fondo_tk7 = fondo_tk7


# Función para iniciar el juego
def iniciar_juego():
    menu_principal.withdraw()  # Ocultar el menú principal
    root.deiconify()  # Mostrar la ventana del juego

# Crear la ventana principal del menú
menu_principal = tk.Tk()
menu_principal.title("Clue: Power Rangers Samurai")
menu_principal.geometry("500x300")
imagen1 = Image.open(resource_path("imagenes/power_rangers.jpg"))
imagen1 = imagen1.resize((500, 300))  # Redimensionar según sea necesario
fondo_tk = ImageTk.PhotoImage(imagen1)
# Crear un label para mostrar la imagen de fondo
label_fondo = tk.Label(menu_principal, image=fondo_tk)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # Ajustar el fondo para cubrir toda la ventana
menu_principal.fondo_tk = fondo_tk

# Menú principal con botones para ver las reglas o iniciar el juego
tk.Label(menu_principal, text="Menú Principal", padx=5, pady=5).pack()

boton_iniciar = tk.Button(menu_principal, text="Iniciar Juego", command=iniciar_juego)
boton_iniciar.pack(pady=60)

boton_reglas = tk.Button(menu_principal, text="Ver Reglas", command=mostrar_reglas)
boton_reglas.pack(pady=5)

# Crear la ventana principal del juego (oculta inicialmente)
root = tk.Toplevel(menu_principal)
root.title("Clue: Power Rangers Samurai")
root.geometry("500x300")
root.withdraw()  # Ocultar la ventana del juego al principio
imagen3 = Image.open(resource_path("imagenes/Santuario.jpg"))
imagen3 = imagen3.resize((500, 300))  # Redimensionar según sea necesario
fondo_tk3 = ImageTk.PhotoImage(imagen3)
# Crear un label para mostrar la imagen de fondo
label_fondo2 = tk.Label(root, image=fondo_tk3)
label_fondo2.place(x=0, y=0, relwidth=1, relheight=1)  # Ajustar el fondo para cubrir toda la ventana

root.fondo_tk3 = fondo_tk3

# Crear botones para seleccionar personajes, armas y locaciones
tk.Label(root, text="Pregunta sobre:", padx=20, pady=10).pack()

boton_personajes = tk.Button(root, text="Personajes", command=lambda: abrir_opciones("personajes", personajes_originales))
boton_personajes.pack(padx=10, pady=5)

boton_armas = tk.Button(root, text="Armas", command=lambda: abrir_opciones("armas", armas_originales))
boton_armas.pack(padx=10, pady=5)

boton_locaciones = tk.Button(root, text="Locaciones", command=lambda: abrir_opciones("locaciones", locaciones_originales))
boton_locaciones.pack(padx=10, pady=5)

# Iniciar el menú principal
menu_principal.mainloop()

# Resto del código sigue igual...

# Para cargar cualquier imagen, simplemente asegúrate de usar resource_path:
# Ejemplo:
# imagen1 = Image.open(resource_path("imagenes/power_rangers.jpg"))
