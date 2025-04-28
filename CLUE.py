import random
import mariadb
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import os

# Cargar variables del entorno
load_dotenv()

# Conexión a la base de datos
conexion = mariadb.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USER'),
    password=os.getenv('PASS'),
    database=os.getenv('DATABASE')
)
cursor = conexion.cursor(dictionary=True)

# Elementos del juego
personajes = ["Don Rafael (Empresario)", "Doña Sofía (Chef)", "Dra. Natalia (Investigadora)", "Sr. Juan (Jardinero)", "Ing. Moisés (Ingeniero)"]
locaciones = ["Sala de estar", "Biblioteca", "Cocina", "Habitación principal", "Jardín"]
armas = ["Cuchillo", "Pistola", "Veneno", "Tijeras", "Cuerda"]

def Generar_caso():
    global culpable, locacion, arma, historias
    num = random.randint(1,5)
    cursor.execute(f"SELECT * FROM casos WHERE id = {num};")
    datos = cursor.fetchone()
    culpable = datos['Personaje']
    locacion = datos['Lugar']
    arma = datos['Arma']
    print(culpable, locacion, arma)
    cursor.execute(f"SELECT * FROM historias WHERE caso_id = {num}")
    historias = cursor.fetchone()
    print(historias['Don Rafael'])
    #Don_Rafael, Dona_Sofia, Dra_Natalia, Sr_Juan, Ing_Moises = historias


# Función para verificar la respuesta del jugador
def verificar_respuesta():
    sospechoso = sospechoso_var.get()
    lugar = lugar_var.get()
    herramienta = herramienta_var.get()
    
    if sospechoso == culpable and lugar == locacion and herramienta == arma:
        messagebox.showinfo("¡Victoria!", f"¡Correcto! El culpable es {culpable}, usó {arma} en {locacion}.")
        root.destroy()
    else:
        global intentos
        intentos -= 1
        if intentos > 0:
            messagebox.showwarning("Incorrecto", f"No es correcto. Te quedan {intentos} intentos.")
        else:
            messagebox.showerror("Derrota", f"Se acabaron tus intentos. El culpable era {culpable}, que usó {arma} en {locacion}.")
            root.destroy()

# Función para mostrar las historias de los personajes
def mostrar_historias():
    Vent_Historia = tk.Toplevel(root)
    Vent_Historia.title("Historias")

    def HistoRafael():
        Vent_Rafa = tk.Toplevel(Vent_Historia)
        Vent_Rafa.title('Testimonio de Don Rafael (Empresario)')
        Rafa_Text = tk.Label(Vent_Rafa, text = historias['Don Rafael'])
        Rafa_Text.pack()
    
    def HistoSofia():
        Vent_Rafa = tk.Toplevel(Vent_Historia)
        Vent_Rafa.title('Testimonio de Don Rafael (Empresario)')
        Rafa_Text = tk.Label(Vent_Rafa, text = historias['Doña Sofía'])
        Rafa_Text.pack()
    
    def HistoNatalia():
        Vent_Rafa = tk.Toplevel(Vent_Historia)
        Vent_Rafa.title('Testimonio de Don Rafael (Empresario)')
        Rafa_Text = tk.Label(Vent_Rafa, text = historias['Dra. Natalia'])
        Rafa_Text.pack()

    def HistoJuan():
        Vent_Rafa = tk.Toplevel(Vent_Historia)
        Vent_Rafa.title('Testimonio de Don Rafael (Empresario)')
        Rafa_Text = tk.Label(Vent_Rafa, text = historias['Sr. Juan'])
        Rafa_Text.pack()
    
    def HistoMoy():
        Vent_Rafa = tk.Toplevel(Vent_Historia)
        Vent_Rafa.title('Testimonio de Don Rafael (Empresario)')
        Rafa_Text = tk.Label(Vent_Rafa, text = historias['Ing. Moisés'])
        Rafa_Text.pack()

    btn_Rafael = tk.Button(Vent_Historia, text = 'Don Rafael (Empresario)', command=HistoRafael, font=("Arial",12), bg="orange",fg='white')
    btn_Rafael.pack(padx=20, pady=20)
    btn_Sofia = tk.Button(Vent_Historia, text = 'Doña Sofía (Chef)', command=HistoSofia, font=("Arial",12), bg="orange",fg='white')
    btn_Sofia.pack(padx=20, pady=20)
    btn_Natalia = tk.Button(Vent_Historia, text = 'Dra. Natalia (Investigadora)', command=HistoNatalia, font=("Arial",12), bg="orange",fg='white')
    btn_Natalia.pack(padx=20, pady=20)
    btn_Juan = tk.Button(Vent_Historia, text = 'Sr. Juan (Jardinero)', command=HistoJuan, font=("Arial",12), bg="orange",fg='white')
    btn_Juan.pack(padx=20, pady=20)
    btn_Moy = tk.Button(Vent_Historia, text = 'Ing. Moisés (Ingeniero)', command=HistoMoy, font=("Arial",12), bg="orange",fg='white')
    btn_Moy.pack(padx=20, pady=20)

# Crear ventana principal
root = tk.Tk()
root.title("Juego estilo Clue")


Generar_caso()
# Variables para las opciones del jugador
sospechoso_var = tk.StringVar()
lugar_var = tk.StringVar()
herramienta_var = tk.StringVar()

# Número de intentos
intentos = 3

# Configuración de la interfaz
tk.Label(root, text="¡CLUE Piraton!", font=("Arial", 16)).pack(pady=10)
tk.Label(root, text=f"¡Atención! Alguien ha asesinado al abogado :c. Investiga quién es el culpable.", font=("Arial", 12)).pack(pady=10)

tk.Button(root, text="Mostrar historias de los personajes", command=mostrar_historias).pack(pady=10)

tk.Label(root, text="Selecciona tus sospechas:", font=("Arial", 12)).pack(pady=5)

tk.Label(root, text="Sospechoso:").pack()
sospechoso_menu = tk.OptionMenu(root, sospechoso_var, *personajes)
sospechoso_menu.pack()

tk.Label(root, text="Lugar:").pack()
lugar_menu = tk.OptionMenu(root, lugar_var, *locaciones)
lugar_menu.pack()

tk.Label(root, text="Arma:").pack()
herramienta_menu = tk.OptionMenu(root, herramienta_var, *armas)
herramienta_menu.pack()

tk.Button(root, text="Enviar", command=verificar_respuesta).pack(pady=10)

# Iniciar el bucle de la interfaz gráfica
root.mainloop()
