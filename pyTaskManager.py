import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry
import threading
import time
import pickle

class Tarea:
    def __init__(self, titulo, descripcion, prioridad, fecha_limite):
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.fecha_limite = fecha_limite

class GestorTareas:
    def __init__(self):
        try:
            with open('tareas.pkl', 'rb') as f:
                self.tareas = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)
        self.guardar_tareas()

    def eliminar_tarea(self, tarea):
        self.tareas.remove(tarea)
        self.guardar_tareas()

    def obtener_tareas(self):
        return self.tareas

    def guardar_tareas(self):
        with open('tareas.pkl', 'wb') as f:
            pickle.dump(self.tareas, f)

class GUI:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Gestor de Tareas")
        self.gestor = GestorTareas()

        # Set the window size to be double the original size
        self.raiz.geometry("800x600")  # Adjust this value as needed

        self.titulo_label = tk.Label(self.raiz, text="Título")
        self.titulo_entrada = tk.Entry(self.raiz)
        self.descripcion_label = tk.Label(self.raiz, text="Descripción")
        self.descripcion_entrada = tk.Entry(self.raiz)
        self.prioridad_label = tk.Label(self.raiz, text="Prioridad")
        self.prioridad_entrada = tk.Entry(self.raiz)
        self.fecha_limite_label = tk.Label(self.raiz, text="Fecha límite")
        self.fecha_limite_entrada = DateEntry(self.raiz, date_pattern='dd-mm-yyyy')
        self.agregar_boton = tk.Button(self.raiz, text="Agregar Tarea", command=self.agregar_tarea)
        self.eliminar_boton = tk.Button(self.raiz, text="Eliminar Tarea", command=self.eliminar_tarea)

        # Set the listbox to be double the original size
        self.lista_tareas = tk.Listbox(self.raiz, selectmode=tk.SINGLE, width=100, height=20)  # Adjust these values as needed
        self.lista_tareas.bind('<<ListboxSelect>>', self.mostrar_info_tarea)

        self.titulo_label.pack()
        self.titulo_entrada.pack()
        self.descripcion_label.pack()
        self.descripcion_entrada.pack()
        self.prioridad_label.pack()
        self.prioridad_entrada.pack()
        self.fecha_limite_label.pack()
        self.fecha_limite_entrada.pack()
        self.agregar_boton.pack()
        self.eliminar_boton.pack()
        self.lista_tareas.pack()

        for tarea in self.gestor.obtener_tareas():
            self.lista_tareas.insert(tk.END, f"{tarea.titulo} - {tarea.fecha_limite.strftime('%d-%m-%Y')}")

    def agregar_tarea(self):
        titulo = self.titulo_entrada.get()
        descripcion = self.descripcion_entrada.get()
        prioridad = self.prioridad_entrada.get()
        fecha_limite = self.fecha_limite_entrada.get_date()
        if titulo and descripcion and prioridad and fecha_limite:
            tarea = Tarea(titulo, descripcion, prioridad, fecha_limite)
            self.gestor.agregar_tarea(tarea)
            self.lista_tareas.insert(tk.END, f"{tarea.titulo} - {tarea.fecha_limite.strftime('%d-%m-%Y')}")
        else:
            messagebox.showerror("Error", "Todos los campos deben estar llenos")

    def eliminar_tarea(self):
        tarea_seleccionada = self.lista_tareas.curselection()
        if tarea_seleccionada:
            tarea = self.gestor.obtener_tareas()[tarea_seleccionada[0]]
            self.gestor.eliminar_tarea(tarea)
            self.lista_tareas.delete(tarea_seleccionada)

    def mostrar_info_tarea(self, event):
        tarea_seleccionada = self.lista_tareas.curselection()
        if tarea_seleccionada:
            tarea = self.gestor.obtener_tareas()[tarea_seleccionada[0]]
            messagebox.showinfo("Información de la Tarea", f"Título: {tarea.titulo}\nDescripción: {tarea.descripcion}\nPrioridad: {tarea.prioridad}\nFecha límite: {tarea.fecha_limite.strftime('%d-%m-%Y')}")
            if tarea.fecha_limite.date() == datetime.now().date():
                self.lista_tareas.itemconfig(tarea_seleccionada, {'bg':'red'})

    def check_upcoming_tasks(self):
        while True:
            now = datetime.now().date()  # Convert 'now' to a date object
            for tarea in self.gestor.obtener_tareas():
                if (tarea.fecha_limite - now).days < 1:
                    messagebox.showinfo("Notificación", f"La tarea {tarea.titulo} vence pronto")
            time.sleep(3600)  # Check every hour

    def generar_grafico(self):
        # This is just a placeholder. You would need to replace this with your actual data.
        data = [tarea.prioridad for tarea in self.gestor.obtener_tareas()]
        fig = plt.Figure(figsize=(6, 5), dpi=100)
        fig.add_subplot(111).bar(range(len(data)), data)
        chart = FigureCanvasTkAgg(fig, self.raiz)
        chart.get_tk_widget().pack()

    def ejecutar(self):
        threading.Thread(target=self.check_upcoming_tasks, daemon=True).start()
        self.raiz.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.ejecutar()