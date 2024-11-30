import tkinter as tk
import mapa


class Windows(tk.Tk):
    nuevoTab = "<F5>"


    segundo = 0
    minuto = 0
    iftimer = False
    ifgame = False

    Buttonsx = 0
    Buttonsy = 0
    encabezadoY = 0
    
    def __init__(self) -> None:
        super().__init__()
        self.title("BuscaMinas")

        # Crear una barra de menú
        self.menu_bar = tk.Menu(self)

        # Crear el menú "Archivo"
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Nuevo Juego "+self.nuevoTab, command=self.RestarTablero)
        file_menu.add_separator()
        file_menu.add_command(label="Principiante", command=self.Principiante)
        file_menu.add_command(label="Intermedio", command=self.Intermedio)
        file_menu.add_command(label="Experto", command=self.Experto)
        file_menu.add_command(label="Personalizado", command=self.personalizado_win)
        file_menu.add_separator()
        file_menu.add_command(label="Mascara", command=self.mascara)
        file_menu.add_separator()
        file_menu.add_command(label="Mejores Tiempos", command=self.ignore)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.destroy)

        # Añadir el menú "Archivo" a la barra de menú
        self.menu_bar.add_cascade(label="Juego", menu=file_menu)

        # Crear el menú "Editar"
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Aumentar", command=self.ignore)
        edit_menu.add_command(label="Reducir", command=self.ignore)
        file_menu.add_separator()
        edit_menu.add_command(label="Pruevas", command=self.ignore)

        # Añadir el menú "Editar" a la barra de menú
        self.menu_bar.add_cascade(label="Opciones", menu=edit_menu)

        # Configurar la barra de menú en la ventana principal
        self.config(menu=self.menu_bar)
    
        self.font = mapa.font.Font(self, family="Trade Gothic Inline", size=16, weight="bold")

        self.tablero = tk.Frame(self)
        self.tablero['height'] = 60


        fr1 = tk.Frame(self.tablero, bg='black')
        fr1.pack(side='left', expand=1, fill='both', ipadx=1, ipady=1)

        self.lb_mine = tk.Label(fr1, text="400/120", font=self.font)
        self.lb_mine.pack(expand=1)

        fr2 = tk.Frame(self.tablero)
        fr2.pack(side='left', expand=1, fill='both', ipadx=1, ipady=1)
        fr3 = tk.Frame(self.tablero, bg='brown3')
        fr3.pack(side='left', expand=1, fill='both', ipadx=1, ipady=1)

        self.lb_time = tk.Label(fr3, text=" 00:00 ", font=self.font)
        self.lb_time.pack(expand=1)


        self.tablero.pack(expand=0, fill='both')

        self.mapa = mapa.Mapa(self, self.perdio, self.gano, self.actualizarTablero)
        self.init_Tablero()

        self.bind(self.nuevoTab, self.nuevoTablero)
        # obtiene los bixeles(Buttonsx, Buttonsy) que ocupa un Button del tablero
        self.after(100, self.pixels)


    def ignore(self, e: tk.Event=None):
        pass

    def press(self, e):
        print('presssssssss')

    def pixels(self):
        self.Buttonsx, self.Buttonsy = self.mapa.getPixelButtons()
        self.encabezadoY = self.winfo_height() - self.mapa.winfo_height()
        # print(self.Buttonsx, self.Buttonsy)

    def fin(self):
        self.iftimer = False

    def perdio(self):
        self.anuncio_win("Perdiste")
        self.ifgame = False

    def gano(self):
        self.anuncio_win("Ganaste")
        self.ifgame = False

    def tempxSegundo(self):
        if self.iftimer and self.ifgame:
            # print(self.iftimer)
            self.after(1000, self.tempxSegundo)
            self.segundo += 1
            if self.segundo == 60:
                self.minuto += 1
                self.segundo = 0
        self.lb_time['text'] = f"{self.minuto:02d}:{self.segundo:02d}"
        
    def actualizarTablero(self):

        if not self.iftimer:
            self.iftimer = True
            if self.ifgame:
                self.after(1000, self.tempxSegundo)

        self.lb_mine['text'] = f"{self.mapa.casillas_abiertas}/{self.mapa.minas}"
        
    def nuevoTablero(self, x: int=None, y: int=None, c: int|None=None):
        self.ifgame = False
        boolTmp = x and y and c
        if boolTmp:
            self.mapa.generar(x, y, c)
        else:
            self.mapa.generar()
        self.actualizarTablero()

        self.minuto = 0
        self.segundo = 0
        self.tempxSegundo()

        self.iftimer = False
        self.ifgame = True

        if boolTmp:
            # self.after(500, self.layout)
            self.layout(x, y) # arreglar el bug!!!!!!!!!!!!!!!!
        else:
            self.mascara()
        
    def init_Tablero(self):
        self.mapa.generar(10, 10, .3)
        self.actualizarTablero()

        self.minuto = 0
        self.segundo = 0
        self.tempxSegundo()

        self.iftimer = False
        self.ifgame = True
        self.mascara()

    def layout(self, x=None, y=None):
        if x is None or y is None:
            # cantidad de minas en columnas y filas
            mx, my = self.mapa.x, self.mapa.y
        else:
            mx, my = x, y

        rootx, rooty = self.winfo_width(), self.winfo_height()

        # suma de todos los pixeles en horizontal
        width = (self.Buttonsx*mx)+(self.mapa.padx*2)
        # suma de todos los pixeles en vertical
        height = (self.Buttonsy*my)+self.encabezadoY+(self.mapa.pady*2)

        if rootx != width or rooty != height:
            if rootx+1 == width or rooty+1 == height:
                self.geometry(f"{rootx + 1}x{rooty + 1}")
                pass
            else:
                self.geometry(f"{(rootx + width) // 2}x{(rooty + height) // 2}")
            self.update_idletasks()
            self.layout(x, y)
            # self.after(100, self.layout, x, y)
        else:
            self.after(500, self.mascara)
        

    def anuncio_win(self, text=None):
        if text is None:
            text = "Prueva"
        toplevel = tk.Toplevel(self)
        toplevel.focus()
        toplevel.overrideredirect(True)

        # toplevel.bind:
        toplevel.bind("<FocusOut>", lambda e: toplevel.destroy(), False)
        toplevel.bind(self.nuevoTab, self.nuevoTablero, False)
        toplevel.bind(self.nuevoTab, lambda e: toplevel.destroy(), True)

        label = tk.Label(toplevel, text=text, font=("Arial", 20))
        label.pack(padx=20, pady=20)

        # Obtener las dimensiones de la ventana principal
        self.update_idletasks()  # Actualizar la geometría de la ventana
        main_width = self.winfo_width() + 16
        main_height = self.winfo_height() + 64
        main_x = self.winfo_x()
        main_y = self.winfo_y()

        # Obtener las dimensiones de la ventana Toplevel
        top_width = toplevel.winfo_reqwidth()
        top_height = toplevel.winfo_reqheight()

        # Calcular la posición centrada
        position_right = main_x + (main_width // 2) - (top_width // 2)
        position_down = main_y + (main_height // 2) - (top_height // 2)

        # Establecer la geometría del Toplevel centrado
        toplevel.geometry(f"{top_width}x{top_height}+{position_right}+{position_down}")
        toplevel.after(3000, toplevel.destroy)
        # toplevel.grab_set()  # Opcional: bloquea antes de cerrar el Toplevel


    # =======================================MENU JUEGO
    def RestarTablero(self):
        self.after(10, self.nuevoTablero)
    def Principiante(self):
        self.after(10, lambda: self.nuevoTablero(10, 10, .2))

    def Intermedio(self):
        self.after(10, lambda: self.nuevoTablero(15, 15, .3))

    def Experto(self):
        self.after(10, lambda: self.nuevoTablero(26, 16, .3))
            
    def personalizado_win(self):
        rootx, rooty = self.winfo_rootx(), self.winfo_rooty()
        toplevel = tk.Toplevel(self, bg="lavender")
        toplevel.focus()
        toplevel.geometry(f"120x120+{rootx}+{rooty}")
        toplevel.overrideredirect(True)

        # toplevel.bind:
        # toplevel.bind("<FocusOut>", lambda e: toplevel.destroy(), False)
        toplevel.bind(self.nuevoTab, self.nuevoTablero, False)
        toplevel.bind(self.nuevoTab, lambda e: toplevel.destroy(), True)
        toplevel.bind("<Escape>", lambda e: toplevel.destroy(), True)

        lb_aviso = tk.Label(toplevel, text="  Esc  ", fg="white", bg="red3")
        lb_aviso.pack(anchor="e")


        fr_width = tk.Frame(toplevel)

        lb_width = tk.Label(fr_width, text=" width:")
        lb_width.pack(side="left")

        en_width = tk.Entry(fr_width, width=5, justify="center")
        en_width.pack()

        fr_width.pack()

        fr_height = tk.Frame(toplevel)

        lb_height = tk.Label(fr_height, text="height:")
        lb_height.pack(side="left")

        en_height = tk.Entry(fr_height, width=5, justify="center")
        en_height.pack()

        fr_height.pack()
        
        fr_mine = tk.Frame(toplevel)

        lb_mine = tk.Label(fr_mine, text="  mine:")
        lb_mine.pack(side="left")

        en_mine = tk.Entry(fr_mine, width=5, justify="center")
        en_mine.pack()

        fr_mine.pack()

        def ejecutar():
            try:
                w = int(en_width.get())
                h = int(en_height.get())
                m = int(en_mine.get())
            except:
                return
            self.nuevoTablero(w, h, m)
            toplevel.destroy()

        bt_ok = tk.Button(toplevel, text="ok", command=ejecutar)
        bt_ok.pack(fill="x", padx=10)

        toplevel.grab_set()  # bloquea antes de cerrar el Toplevel
    
    # ============================================================

    def mascara(self, veces=1, color="LightSteelBlue3", ms=1000):
        if color is None:
            for bt in self.mapa.minasBT:
                bt.config(bg="SystemButtonFace")

        elif veces != 0:
            for bt in self.mapa.minasBT:
                bt.config(bg=color)
            self.after(ms//2, self.mascara, veces-1, None, ms)
            self.after(ms, self.mascara, veces-1, color, ms)
        


if __name__ == "__main__":
    # print(dir(tk))
    ven = Windows()
    ven.mainloop()
