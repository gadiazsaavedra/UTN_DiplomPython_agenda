from tkinter import Tk, Button, Entry, Label, PhotoImage, ttk
from tkinter import StringVar, Scrollbar, Frame, messagebox

# from conexion_sqlite import Comunicacion
from time import strftime
import pandas as pd

######### CONEXION SQLITE###################
import sqlite3


class Comunicacion:
    def __init__(self):
        self.conexion = sqlite3.connect("base_datos.db")

    def inserta_datos(self, nombre, edad, correo, telefono):
        cursor = self.conexion.cursor()

        bd = """INSERT INTO datos (NOMBRE, EDAD, CORREO, TELEFONO)
        VALUES('{}','{}','{}','{}')""".format(
            nombre, edad, correo, telefono
        )
        cursor.execute(bd)
        self.conexion.commit()
        cursor.close()

    def mostrar_datos(self):
        cursor = self.conexion.cursor()
        bd = "SELECT*FROM datos"
        cursor.execute(bd)
        return cursor.fetchall()

    def elimina_datos(self, nombre):
        cursor = self.conexion.cursor()
        bd = f"""DELETE FROM datos WHERE NOMBRE='{nombre}' """
        cursor.execute(bd)
        self.conexion.commit()
        cursor.close()

    def actualiza_datos(self, ID, nombre, edad, correo, telefono):
        cursor = self.conexion.cursor()
        bd = """UPDATE datos SET NOMBRE='{}', EDAD='{}', CORREO='{}', TELEFONO='{}'
        WHERE ID='{}' """.format(
            nombre, edad, correo, telefono, ID
        )
        cursor.execute(bd)
        dato = cursor.rowcount
        self.conexion.commit()
        cursor.close()
        return dato


##########MAIN.PY############################
class Ventana(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.nombre = StringVar()
        self.edad = StringVar()
        self.correo = StringVar()
        self.telefono = StringVar()

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=5)
        self.base_datos = Comunicacion()

        self.widgets()

    def widgets(self):
        self.frame_uno = Frame(self.master, bg="pink", height=200, width=800)
        self.frame_uno.grid(row=0, column=0, sticky="nsew")
        self.frame_dos = Frame(self.master, bg="white", height=300, width=800)
        self.frame_dos.grid(row=1, column=0, sticky="nsew")

        self.frame_uno.columnconfigure([0, 1, 2], weight=1)
        self.frame_uno.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)
        self.frame_dos.columnconfigure([0], weight=1)
        self.frame_dos.rowconfigure([0], weight=1)

        Label(
            self.frame_uno,
            text="Opciones",
            bg="white",
            fg="black",
            font=("Kaufmann BT", 13, "bold"),
        ).grid(column=2, row=0)
        Button(
            self.frame_uno,
            text="REFRESCAR LISTA DE DATOS",
            font=("Arial", 9, "bold"),
            command=self.actualizar_tabla,
            fg="black",
            bg="deep sky blue",
            width=20,
            bd=3,
        ).grid(column=2, pady=5)

        Label(
            self.frame_uno,
            text="Agregar y actualizar datos",
            fg="black",
            bg="white",
            font=("Kaufmann BT", 13, "bold"),
        ).grid(columnspan=2, column=0, row=0, pady=5)
        Label(
            self.frame_uno,
            text="NOMBRE",
            fg="black",
            bg="white",
            font=("Arial", 13, "bold"),
        ).grid(column=0, row=1, pady=5)
        Label(
            self.frame_uno,
            text="EDAD",
            fg="black",
            bg="white",
            font=("Arial", 13, "bold"),
        ).grid(column=0, row=2, pady=5)
        Label(
            self.frame_uno,
            text="MAIL",
            fg="black",
            bg="white",
            font=("Arial", 13, "bold"),
        ).grid(column=0, row=3, pady=5)
        Label(
            self.frame_uno,
            text="TELEFONO",
            fg="black",
            bg="white",
            font=("Arial", 13, "bold"),
        ).grid(column=0, row=4, pady=5)

        Entry(
            self.frame_uno,
            textvariable=self.nombre,
            font=("Comic Sans MS", 12),
            highlightbackground="deep sky blue",
            highlightthickness=5,
        ).grid(column=1, row=1)
        Entry(
            self.frame_uno,
            textvariable=self.edad,
            font=("Comic Sans MS", 12),
            highlightbackground="deep sky blue",
            highlightthickness=5,
        ).grid(column=1, row=2)
        Entry(
            self.frame_uno,
            textvariable=self.correo,
            font=("Comic Sans MS", 12),
            highlightbackground="deep sky blue",
            highlightthickness=5,
        ).grid(column=1, row=3)
        Entry(
            self.frame_uno,
            textvariable=self.telefono,
            font=("Comic Sans MS", 12),
            highlightbackground="deep sky blue",
            highlightthickness=5,
        ).grid(column=1, row=4)

        Button(
            self.frame_uno,
            text="AÑADIR DATOS",
            font=("Arial", 9, "bold"),
            bg="deep sky blue",
            width=20,
            bd=3,
            command=self.agregar_datos,
        ).grid(column=2, row=2, pady=5, padx=5)
        Button(
            self.frame_uno,
            text="LIMPIAR CAMPOS",
            font=("Arial", 9, "bold"),
            bg="deep sky blue",
            width=20,
            bd=3,
            command=self.limpiar_campos,
        ).grid(column=2, row=3, pady=5, padx=5)
        Button(
            self.frame_uno,
            text="EDITAR-ACTUALIZA BASE DATOS",
            font=("Arial", 9, "bold"),
            bg="deep sky blue",
            width=20,
            bd=3,
            command=self.actualizar_datos,
        ).grid(column=2, row=4, pady=5, padx=5)
        Button(
            self.frame_uno,
            text="EXPORTAR A EXCEL",
            font=("Arial", 9, "bold"),
            bg="deep sky blue",
            width=20,
            bd=3,
            command=self.guardar_datos,
        ).grid(column=2, row=5, pady=5, padx=5)

        estilo_tabla = ttk.Style()
        estilo_tabla.configure(
            "Treeview",
            font=("Helvetica", 20, "bold"),
            foreground="black",
            background="white",
        )
        estilo_tabla.map(
            "Treeview",
            background=[("selected", "deep sky blue")],
            foreground=[("selected", "black")],
        )
        estilo_tabla.configure(
            "Heading",
            background="white",
            foreground="black",
            padding=3,
            font=("Arial", 20, "bold"),
        )

        self.tabla = ttk.Treeview(self.frame_dos)
        self.tabla.grid(column=0, row=0, sticky="nsew")
        ladox = ttk.Scrollbar(
            self.frame_dos, orient="horizontal", command=self.tabla.xview
        )
        ladox.grid(column=0, row=1, sticky="ew")
        ladoy = ttk.Scrollbar(
            self.frame_dos, orient="vertical", command=self.tabla.yview
        )
        ladoy.grid(column=1, row=0, sticky="ns")
        self.tabla.configure(xscrollcommand=ladox.set, yscrollcommand=ladoy.set)

        self.tabla["columns"] = ("Edad", "Correo", "Telefono")
        self.tabla.column("#0", minwidth=100, width=120, anchor="center")
        self.tabla.column("Edad", minwidth=100, width=120, anchor="center")
        self.tabla.column("Correo", minwidth=100, width=120, anchor="center")
        self.tabla.column("Telefono", minwidth=100, width=120, anchor="center")

        self.tabla.heading("#0", text="NOMBRE", anchor="center")
        self.tabla.heading("Edad", text="EDAD", anchor="center")
        self.tabla.heading("Correo", text="MAIL", anchor="center")
        self.tabla.heading("Telefono", text="TELEFONO", anchor="center")

        self.tabla.bind("<<TreeviewSelect>>", self.obtener_fila)
        self.tabla.bind("<Double-1>", self.eliminar_datos)

    def obtener_fila(self, event):
        item = self.tabla.focus()
        self.data = self.tabla.item(item)
        if self.data["values"]:
            self.nombre.set(self.data["text"])
            self.edad.set(self.data["values"][0])
            self.correo.set(self.data["values"][1])
            self.telefono.set(self.data["values"][2])

    def eliminar_datos(self, event):
        self.limpiar_campos()
        item = self.tabla.selection()[0]
        x = messagebox.askquestion("Informacion", "Desea Continuar?")
        if x == "yes":
            self.tabla.delete(item)
            self.base_datos.elimina_datos(self.data["text"])

    def agregar_datos(self):
        nombre = self.nombre.get()
        edad = self.edad.get()
        correo = self.correo.get()
        telefono = self.telefono.get()
        datos = (edad, correo, telefono)
        if nombre and edad and correo and telefono != "":
            self.tabla.insert("", 0, text=nombre, values=datos)
            self.base_datos.inserta_datos(nombre, edad, correo, telefono)
            self.limpiar_campos()

    def actualizar_tabla(self):
        self.limpiar_campos()
        datos = self.base_datos.mostrar_datos()
        self.tabla.delete(*self.tabla.get_children())
        for dato in datos:
            text = dato[1:2][0]
            values = dato[2:5]
            self.tabla.insert("", "end", text=text, values=values)

    def actualizar_datos(self):
        item = self.tabla.focus()
        self.data = self.tabla.item(item)
        nombre = self.data["text"]
        datos = self.base_datos.mostrar_datos()
        for fila in datos:
            nombre_bd = fila[1]
            if nombre_bd == nombre:
                Id = fila[0]
                if Id != None:
                    nombre = self.nombre.get()
                    edad = self.edad.get()
                    correo = self.correo.get()
                    telefono = self.telefono.get()
                    if nombre and edad and correo and telefono != "":
                        self.base_datos.actualiza_datos(
                            Id, nombre, edad, correo, telefono
                        )
                        self.tabla.delete(*self.tabla.get_children())
                        datos = self.base_datos.mostrar_datos()
                        i = -1
                        for dato in datos:
                            i = i + 1
                            self.tabla.insert(
                                "", i, text=datos[i][1:2][0], values=datos[i][2:5]
                            )

    def limpiar_campos(self):
        self.nombre.set("")
        self.edad.set("")
        self.correo.set("")
        self.telefono.set("")

    def guardar_datos(self):
        self.limpiar_campos()
        datos = self.base_datos.mostrar_datos()
        nombre, edad, correo, telefono = list(zip(*datos))[1:5]
        fecha = strftime("%d-%m-%y_%H-%M-%S")
        datos = {
            "Nombre": nombre,
            "Edad": edad,
            "Correo": correo,
            "Telefono": telefono,
        }
        df = pd.DataFrame(datos, columns=["Nombre", "Edad", "Correo", "Telefono"])
        df.to_excel(f"DATOS {fecha}.xlsx")
        messagebox.showinfo("Informacion", "Datos guardados")


if __name__ == "__main__":
    ventana = Tk()
    ventana.title("")
    ventana.minsize(height=400, width=600)
    ventana.geometry("800x500")
    ventana.call("wm", "iconphoto", ventana._w, PhotoImage(file="logo.png"))
    app = Ventana(ventana)
    app.mainloop()
