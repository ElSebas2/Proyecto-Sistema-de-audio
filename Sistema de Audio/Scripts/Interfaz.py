import tkinter as tk
from tkinter import filedialog
import os
from tkinter import simpledialog
import audfunc as af
import multiprocessing
global numSensor

"""root_dialog = tk.Tk()
root_dialog.withdraw()  # Ocultar la ventana raíz

# Mostrar una ventana de diálogo que pide al usuario que ingrese la cantidad de sensores
cant_sensores = simpledialog.askinteger("Cantidad de Sensores", "Por favor, ingresa la cantidad de sensores:", parent=root_dialog)
cant_sensores+=1

# Cerrar la ventana raíz después de que el usuario haya ingresado la cantidad de sensores
root_dialog.destroy()
"""

root = tk.Tk()
root.geometry('1500x700')
cant_sensores=2
# Calcular el tamaño de cada sección
ancho_total = 1500
ancho_seccion1 = int((2 / 3) * ancho_total) - 1  # Restamos 1 para hacer espacio para la línea
ancho_linea = 5  # Ancho de la línea
ancho_seccion2 = ancho_total - ancho_seccion1
cant_col = 2

# Crear la primera sección
seccion1 = tk.Canvas(root, width=ancho_seccion1, height=700, bg='#FFFF86')
seccion1.pack(side='right', fill='both')

# Crear la línea
linea = tk.Canvas(root, width=ancho_linea, height=700, bg='black')
linea.pack(side='right', fill='both')

# Crear un texto en la sección 2
texto_seccion2 = tk.Label(root, text="Sensores en Línea", font=("Helvetica", 16), width= 200)
texto_seccion2.pack(side='top', anchor='n')  # Ubicar el texto en la parte superior centro de la sección 2
texto_seccion2.config(bg='#99D9EA')

# Crear la segunda sección
seccion2 = tk.Canvas(root, width=ancho_seccion2, height=700, bg='#99D9EA')
seccion2.pack(side='right', fill='both')



# Crear una tabla en la sección 1
tabla1 = tk.Frame(seccion1)
tabla1.place(relx=0.5, rely=0.5, anchor='center')  # Centrar la tabla en la sección 1


titulos = ['|Insertar Audio|', '|Sensores|']  # Los títulos de las celdas de la primera fila
tabla_seccion2 = tk.Frame(seccion2)
tabla_seccion2.place(relx=0.5, rely=0.5, anchor='center')  # Centrar la tabla en la sección 2
cant_col_seccion2 = 2
titulos2 = ["Estado", "Sensores"]

for i in range(cant_sensores):
    for j in range(cant_col_seccion2):
        celda = tk.Frame(tabla_seccion2, width=int(0.85*ancho_seccion2/cant_col_seccion2), height=int(0.85*700/cant_sensores), bg='white',bd=1, relief="solid")
        celda.grid(row=i, column=j)  # Ubicar la celda en la posición correspondiente en la tabla
        if i == 0:  # Si estamos en la primera fila...
            texto = titulos2[cant_col_seccion2 - j - 1]  # ...agregar el título correspondiente (de derecha a izquierda)
            etiqueta = tk.Label(celda, text=texto, font=("Helvetica",16))
            etiqueta.pack()
        if titulos2[cant_col_seccion2 - j - 1] == 'Sensores' and i != 0:
            etiquete = tk.Label(celda, text="Sensor" + str(i), font=("Helvetica",16) )
            etiquete.pack()   
        if titulos2[cant_col_seccion2 - j - 1] == 'Estado' and i != 0:
            if af.audio_playing.value == True:
                color = 'green'
            else:
                color = 'red'
            etiqueta_estado = tk.Label(celda, text="         ", font=("Helvetica",16), bg=color,bd=2, relief="solid")
            etiqueta_estado.pack()
            



titulos_ventana = ['|Estado|','|Audios|']
botones = []
def abrir_audio(sensor):
    global numSensor
    new_window = tk.Toplevel(root)
    new_window.configure(background='yellow')
    new_window.title("Gestion de audios")
    numSensor = str(sensor)

    width = int(root.winfo_screenwidth() * 0.8)
    height = int(root.winfo_screenheight() * 0.8)
    new_window.geometry(f'{width}x{height}')
    cant_filas2 = 2
    # Crear una tabla de 2x2
    tabla = tk.Frame(new_window)
    for i in range(cant_filas2):
        for j in range(1):
            celda2 = tk.Frame(tabla, width=int(0.85*ancho_seccion1/cant_col), height=int(0.9*700/cant_sensores), bg='white',bd=2, relief="solid")
            celda2.grid(row=i, column=j)
            if i == 0:
                texto = titulos_ventana[2 - j - 1]
                etiqueta = tk.Label(celda2, text=texto, font=("Helvetica",16))
                etiqueta.pack()  
            if titulos_ventana[2 - j - 1] == '|Audios|' and i != 0:  # Si estamos en la columna "Audios"...
                boton2 = tk.Button(celda2, text="Select Audio", command=lambda row=i: select_audio(boton2,sensor,tabla))
                boton2.pack()  
                   

    tabla.place(relx=0.5, rely=0.5, anchor='center')


def select_audio(button,sensor,tabla):
    filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    nameAud = os.path.basename(filename)
    if filename:
        button.destroy()
        label = tk.Label(button.master, text=os.path.basename(filename), font=("Helvetica", 16))
        label.pack()
        addrow(sensor,tabla)
        with open('audios.txt', 'a') as f:  # Cambia 'output.txt' al nombre de tu archivo
            f.write(                  nameAud +"\t" + filename + '\n')  # Escribe el nombre del archivo en el archivo .txt
                    #numSensor + '\t'+ 
def addrow(row, tabla):
    # Obtener el número actual de filas en la tabla
    num_filas = len(tabla.grid_slaves())

    # Crear una nueva fila en la tabla
    nueva_fila = tk.Frame(tabla, width=int(0.85 * ancho_seccion1 / cant_col), height=int(0.9 * 700 / cant_sensores), bg='white',bd=2, relief="solid")
    nueva_fila.grid(row=num_filas, column=0)
    # Agregar un botón "Select Audio" en la nueva fila
    boton_nuevo = tk.Button(nueva_fila, text="Select Audio", command=lambda: select_audio(boton_nuevo, row, tabla))
    boton_nuevo.pack()
    
    # Añadir la nueva fila a la tabla
    tabla.grid_rowconfigure(num_filas, weight=100)
    tabla.grid_columnconfigure(0, weight=100)



    
        

for i in range(cant_sensores):
    for j in range(cant_col):
        celda = tk.Frame(tabla1, width=int(0.85*ancho_seccion1/cant_col), height=int(0.9*700/cant_sensores), bg='white',bd=2, relief="solid")
        celda.grid(row=i, column=j)  # Ubicar la celda en la posición correspondiente en la tabla
        if i == 0:  # Si estamos en la primera fila...
            texto = titulos[cant_col - j - 1]  # ...agregar el título correspondiente (de derecha a izquierda)
            etiqueta = tk.Label(celda, text=texto, font=("Helvetica",16))
            etiqueta.pack()

        if titulos[cant_col - j - 1] == '|Insertar Audio|' and i != 0:  # Si estamos en la columna "Insertar Audio"...
            boton = tk.Button(celda, text='Subir audio', command=lambda row=i: abrir_audio(row))
            boton.pack()
        if titulos[cant_col - j - 1] == '|Sensores|' and i != 0 :
            etiqueta = tk.Label(celda, text= 'Sensor' + str(i), font=("Helvetica",16))
            etiqueta.pack()



# Ejecutar la ventana
def run_App():
    root.mainloop()
