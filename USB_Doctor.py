#Derechos de autor (c) 2025, Alfonso Angel Mosquera Alvárez
#Todos los derechos reservados.
#Este proyecto llamdo USB Doctor fue creado a partir de un script en pyhton para la reparacion de USB infectados por virus

import os
import sys
import subprocess
import logging
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk, scrolledtext

def configurar_logs():
    logging.basicConfig(
        filename="usb_doctor.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def detectar_unidad_usb():
    unidades = []
    for letra in "DEFGHIJKLMNOPQRSTUVWXYZ":
        if os.path.exists(f"{letra}:"):
            unidades.append(f"{letra}:")
    return unidades

def actualizar_progreso(valor):
    progress_bar["value"] = valor
    root.update_idletasks()

def loggear_y_mostrar(mensaje):
    log_text.insert(tk.END, mensaje + "\n")
    log_text.see(tk.END)
    logging.info(mensaje)
    
# Restaurar visibilidad de archivos

def restaurar_visibilidad_de_archivos(usb_path):
    try:
        loggear_y_mostrar(f"Restaurando visibilidad de archivos en {usb_path}...")
        subprocess.run(["attrib", "/S", "/D", "-r", "-s", "-h", f"{usb_path}\\*.*"], shell=True)
        actualizar_progreso(30)
        loggear_y_mostrar("Visibilidad de archivos restaurada correctamente.")
    except Exception as e:
        logging.error(f"Error al restaurar visibilidad de archivos: {e}")
        messagebox.showerror("Error", f"Error al restaurar visibilidad de archivos: {e}")

# Eliminar accesos directos

def eliminar_accesos_directos(usb_path):
    try:
        loggear_y_mostrar("Eliminando accesos directos...")
        for archivo in Path(usb_path).glob("*.lnk"):
            archivo.unlink()
        actualizar_progreso(50)
        loggear_y_mostrar("Accesos directos eliminados correctamente.")
    except Exception as e:
        logging.error(f"Error al eliminar accesos directos: {e}")
        messagebox.showerror("Error", f"Error al eliminar accesos directos: {e}")

def iniciar_proceso():
    unidades = detectar_unidad_usb()
    if not unidades:
        messagebox.showwarning("Sin Dispositivos", "No se detectaron unidades USB.")
        return
    
    seleccion = combo_unidades.get()
    if not seleccion:
        messagebox.showwarning("Selección Inválida", "Seleccione una unidad antes de continuar.")
        return
    
    actualizar_progreso(10)
    restaurar_visibilidad_de_archivos(seleccion)
    eliminar_accesos_directos(seleccion)
    actualizar_progreso(100)
    messagebox.showinfo("Proceso Completado", "Reparación de USB finalizada.")

def crear_interfaz():
    global combo_unidades, progress_bar, log_text, root
    root = tk.Tk()
    root.title("USB Doctor")
    root.geometry("450x400")
    root.resizable(False, False)
    
    # Ruta del icono
    ruta_icono = r"C:\Users\Alfonso\OneDrive\Escritorio\Auditorias\1 SCRIPTS PYTHON ORIENTADO A LA C-SEGURIDAD\USB Doctor\usb_doctor_icon.ico"
    if os.path.exists(ruta_icono):
        root.iconbitmap(ruta_icono)
    else:
        print("Advertencia: No se encontró el archivo del icono.")
    
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10), padding=5)
    style.configure("TLabel", font=("Arial", 10))
    
    tk.Label(root, text="Seleccione la unidad USB:").pack(pady=5)
    unidades = detectar_unidad_usb()
    combo_unidades = ttk.Combobox(root, values=unidades, state="readonly")
    combo_unidades.pack(pady=5)
    
    btn_iniciar = ttk.Button(root, text="Reparar USB", command=iniciar_proceso)
    btn_iniciar.pack(pady=10)
    
    progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
    progress_bar.pack(pady=5)
    
    log_text = scrolledtext.ScrolledText(root, width=50, height=10, state="normal")
    log_text.pack(pady=5)
    
    root.mainloop()

def main():
    configurar_logs()
    crear_interfaz()

if __name__ == "__main__":
    main()


