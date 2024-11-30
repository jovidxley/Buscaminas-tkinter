import tkinter as tk
from tkinter import font
from random import choice as ch
# from main import Windows


class ButtonMine(tk.Button):

    def __init__(self, patherFr, idx: int, idy: int, mine: bool, mapa, ifont, img_flag, img_mina, img_minas) -> None:
        super().__init__(patherFr, font=ifont, border=2)
        # posicion a la qu pertenece
        self.idx, self.idy = idx, idy

        # valores por defecto para un cuadrado
        self['height'] = 1
        self['width'] = 2

        self.val = 0
        self.val_flag = False

        # las imagenes para los estados
        self.flag, self.mina, self.minas = img_flag, img_mina, img_minas

        # valor que indica si se tiene una mina
        self.mine = mine

        self.mapa = mapa
        self.pack(side='left', ipadx=0, ipady=0, expand=0)

        self.activate()

        self.bind('<Leave>', self.ignorar, False) # Ignorar el evento de salir con el mouse
        self.bind("<Enter>", self.ignorar, False)  # Ignorar el evento de entrar con el mouse
        self.bind("<Motion>", self.ignorar, False) # Ignorar el movimiento del ratón

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        if self.mine:
            return 'X'
        return str(self.val)

    def __bool__(self):
        if self.mine is None:
            return False
        return self.mine

    def ignorar(self, e: tk.Event):
        pass

    def pack_defecto(self):
        self.pack(side='left', ipadx=0, ipady=0)

    def pressflagButton(self):
        if self.val_flag:
            self['relief'] = 'raised'

    def pressButton(self, e: tk.Event=None):
        self['relief'] = 'sunken'

    def normalButton(self, e: tk.Event=None):
        self['relief'] = 'raised'

    def activate(self):
        self.bind('<ButtonRelease-1>', self.bindButton, False) # clic izquierdo
        self.bind('<ButtonPress-1>', self.after(10, self.pressflagButton), False) # clic izquierdo
        self.bind('<ButtonRelease-3>', self.bindButtonFlag, False) # clic derecho

    def deactivate(self):
        self.bind('<ButtonRelease-1>', self.ignorar, False) # clic izquierdo
        self.bind('<ButtonPress-1>', self.ignorar, False) # clic izquierdo
        self.bind('<ButtonRelease-3>', self.ignorar, False) # clic derecho

    def ifgano(self):
        self.mapa.after(10, self.mapa.ifgano)

    def bindButton(self, e: tk.Event=None):
        """muestra el valor de la casilla si no tiene la bandera o no se mostro aun""" # mostrarMinasAft
        if not self.val_flag and self['text'] in ('', '?'):
            if self.mine:
                # si la funcion fue llamada por el usuario, es decir el bind
                if e is not None:
                    # inicia el bucle para apretar(mostrar) todas las casillas
                    self.mapa.after(10, self.mapa.mostrarAft) # PERDIO!!
                    # muestra la mina explotada
                    self['image'] = self.mina

                # o si la funcion fue llamada por otra funcionalidad
                elif self['image'] == '':
                    # muestra la mina normal
                    self['image'] = self.minas

                # se cambian estos parametros para evitar la distorcion de la casilla
                # al introducir la imagenen
                self['height'] = 17
                self['width'] = 20

            else:
                if self.val == 0:
                    # inicia el bucle para mostrar todas las casillas vacias
                    self.mapa.after(10, lambda: self.mapa.mostrarZerosAft(self.idx, self.idy))
                try:
                    # cambia el color de la fuente en funcion a su valor
                    self['fg'] = self['activeforeground'] = self.mapa.valor_color[self.val]
                    # self['fg'] # por defecto
                    # self['activeforeground'] # cuando el mouse pasa encima
                except Exception:
                    print("No es posible asignarle un color:")
                    input(f"valor={self.val} / pos= {self.idx}-{self.idy}")
                
                self['text'] = self.val
                self.mapa.casillas_abiertas -= 1
            # cambia el estilo de la casilla
            self.after(10, func=self.pressButton)
            self.ifgano()

    def bindButtonFlag(self, e: tk.Event):
        """pone o quita la bandera y la interrogante, en la casilla si no se mostro el valor aun"""
        if self['image'] == '' and self['text'] == '' and self.mapa.minas != 0:
            # resta al conteno de minas para el usuario
            self.mapa.minas -= 1

            self.val_flag = True

            self['image'] = self.flag
            self['height'] = 17
            self['width'] = 20

        elif self['text'] in ('', '?'):

            if self.val_flag:
                self['text'] = '?'
                # suma al conteno de minas para el usuario
                self.mapa.minas += 1

                self.val_flag = False
            else:
                self['text'] = ''

            self['image'] = ''
            self['height'] = 1
            self['width'] = 2
            self.after(10, func=self.normalButton)
        self.ifgano()

        # print(f"minas: {self.mapa.minas}")

    def restart(self, mine: bool):
        """restablece la casilla"""
        self.mine = mine
        self.val = 0
        self.val_flag = False
        self['fg'] = self['activeforeground'] = 'SystemButtonText'
        self['text'] = ''
        self['image'] = ''
        self['height'] = 1
        self['width'] = 2
        self.after(10, func=self.normalButton)
        self.activate()


class Mapa(tk.Frame):
    padx= 2
    pady= 2
    x, y = 0, 0
    matrix: list[list[ButtonMine]] = []
    minasBT: list[ButtonMine] = []
    # porcentaje(.0 - 1.0) o cantidad(0 - casillas total) de casillas con minas
    mina_porcentual: float|int = .0
    casillas: int =  0 # x * y
    # cantidad de minas
    minas: int = 0 # int(casillas * mina_porcentual)
    casillas_abiertas: int = 0 # casillas - minas
    
    def __init__(self, father: tk.Tk, perderFun, ganarFun, actualizar, width=None, height=None, porcentual=None) -> None:
        super().__init__(father, padx=self.padx, pady=self.pady, bg="RoyalBlue")
        self.perdio = perderFun
        self.gano = ganarFun
        self.tableroDatos = actualizar

        self.valor_color = dict(zip((0, 1, 2, 3, 4, 5, 6, 7, 8), ('SystemButtonFace', 'blue2', 'green', 'red', 'blue4', 'brown4', 'cyan4', 'black', 'snow4')))
        self.font = font.Font(self, family="OCR A Extended", size=9, weight="bold")
        self.img_flag = tk.PhotoImage(master=self, file="templates/flag.gif")
        self.img_mina = tk.PhotoImage(master=self, file="templates/mina.gif")
        self.img_minas = tk.PhotoImage(master=self, file="templates/minas.gif")

        self.pack()
        if isinstance(width, int) and isinstance(height, int) and isinstance(porcentual, (int, float)):
            self.generar(width, height, porcentual)

    def __str__(self):
        """al imrpimir este objeto, se imprime el tablero de forma ordenada"""
        for yy in self.matrix[:self.y]:
            print(yy[:self.x])
        return ''

    def automatic(self):
        print("macro")

    def getPixelButtons(self):
        if self.matrix != []:
                bt = self.matrix[0][0]
                return (bt.winfo_width(), bt.winfo_height())
        return (0, 0)

    def generar_Button(self, pather, idx, idy):
        """genera y devuelve los botones con parametros por defectos"""
        # valor sin mina
        ifMine = False
        bu = ButtonMine(pather, idx, idy, ifMine, self, self.font, 
                        self.img_flag, self.img_mina, self.img_minas)
        
        return bu

    def modificar_tablero(self):
        """modifica lo que ve el usuario, adapta al nuevo tamanio del tablero"""

        tamanioY = len(self.matrix)

        for yy in range(self.y):

            # si ya se excedio el rango de filas existentes.
            if yy >= tamanioY:
                # crea la lista de Botones para self.matrix
                l = []
                fr = tk.Frame(self)
                
                # agrega filas y columnas faltantes
                for xx in range(self.x):
                    b = self.generar_Button(fr, xx, yy)
                    b.restart(False)
                    l.append(b)
                self.matrix.append(l)
                fr.pack(expand=0)
                # fr.pack_propagate(False)

            # se esta en las filas existentes
            else:
                # agrega los botones faltantes
                tamanioX = len(self.matrix[yy])
                diferenciaX = self.x - tamanioX
                fr = self.matrix[yy][0].master

                for xx in range(tamanioX, tamanioX+diferenciaX):
                    b = self.generar_Button(fr, xx, yy)
                    b.restart(False)
                    self.matrix[yy].append(b)

            # todas las filas que se muestran.
            self.matrix[yy][0].master.pack()

            # en cada fila se muestra x casillas
            for Bt in self.matrix[yy][:self.x]:
                Bt.pack_defecto()

            # en cada fila se ocultan x casillas
            for Bt in self.matrix[yy][self.x:]:
                Bt.pack_forget()

        # todas las filas que se ocultan
        for fL in self.matrix[self.y:]:
            fL[0].master.pack_forget()

    def restart_tablero(self, defecto: bool|None=None):
        """restablece todas las minas en el tablero actual, puede ser aleatorio o true o false"""
        fun = defecto
        ix = self.x
        iy = self.y
        self.minasBT = []

        if defecto is not None:
            for yy in range(iy):
                for xx in range(ix):
                    self.matrix[yy][xx].restart(fun)
                    # self.minasBT.append(self.matrix[y][x])
            return

        
        matrix = [(x, y) for x in range(ix) for y in range(iy)]
        indices = [i for i in range(ix * iy)]
        
        while self.minas != 0:
            pos = ch(indices)
            x, y = matrix.pop(pos)
            self.matrix[y][x].restart(True)
            self.minasBT.append(self.matrix[y][x])
            indices.pop()
            # y = pos // iy
            # x = pos % iy
            self.minas -= 1

    def generar(self, x: int=None, y: int=None, porcentual: float | int=None):
        """Pass"""
        conf_tamanio = False # verifica si se quiere cambiar el tamanio x o y para modificarlo o solo resetear valores
        self.restart_tablero(False) # limpia las minas del tablero actual
        if x is not None:
            if x != self.x:
                conf_tamanio = True
            self.x = x
        if y is not None:
            if y != self.y:
                conf_tamanio = True
            self.y = y

        self.casillas = self.x * self.y

        if type(porcentual) is int:
            self.mina_porcentual = porcentual
            self.minas = porcentual

        elif type(porcentual) is float:
            self.mina_porcentual = porcentual
            self.minas = int(self.casillas * self.mina_porcentual)

        elif type(self.mina_porcentual) is float:
            self.minas = int(self.casillas * self.mina_porcentual)
        
        elif type(self.mina_porcentual) is int:
            self.minas = self.mina_porcentual
        
        else:
            raise TimeoutError("self.minas, no se a actualizado!!")

        minas = self.minas
        if conf_tamanio:
            self.modificar_tablero()
            # restableser valor, por si se creo botones en la modificacion
            self.minas = minas
            self.restart_tablero()
        else:
            self.restart_tablero()

        self.minas = minas
        self.casillas_abiertas = self.casillas - self.minas

        for iy, yy in enumerate(self.matrix[:self.y]):
            # print(iy, yy)
            for ix, xx in enumerate(yy[:self.x]):
                # print(xx)
                if xx.mine:
                    derecha = False
                    izquierda = False
                    arriba = False
                    abajo = False
                    if ix+1 < self.x:
                        derecha = True #revisar borde a la derecha
                        yy[ix+1].val += 1
                    if 0 <= ix-1:
                        izquierda = True #revisar borde a la izquierda
                        yy[ix-1].val +=1

                    if 0 <= iy-1:
                        arriba = True #revisar borde de arriba
                        self.matrix[iy-1][ix].val += 1

                    if arriba and derecha:
                        self.matrix[iy-1][ix+1].val += 1
                    if arriba and izquierda:
                        self.matrix[iy-1][ix-1].val += 1
                    
                    if iy+1 < self.y:
                        abajo = True #revisar borde de abajo
                        self.matrix[iy+1][ix].val += 1
                        
                    if abajo and derecha:
                        self.matrix[iy+1][ix+1].val += 1
                    if abajo and izquierda:
                        self.matrix[iy+1][ix-1].val += 1

        # print(self)

    def mostrarTodo(self): # no en uso!
        """muestra(activa) todo el tablero"""
        for yy in self.matrix[:self.y]:
            for xx in yy[:self.x]:
                xx: ButtonMine
                xx.bindButton()

    def mostrarMinas(self):
        """muestra(activa) todas las minas del tablero"""
        for yy in self.matrix[:self.y]:
            for xx in yy[:self.x]:
                xx: ButtonMine
                if xx.mine == True:
                    xx.bindButton()
                else:
                    xx.pressButton()
                xx.deactivate()

    def mostrarAft(self):
        self.after(10, self.mostrarMinas)
        # print("perdio!!!!!!!!!!!")
        self.perdio()

    def terminarPartida(self):
        self.after(10, self.mostrarMinas)
        # print("gano!!!!!!!!!!!")
        self.gano()

    def ifgano(self):
        # funcion que actualiza el tablero de afuera
        self.tableroDatos()
        # si ya no le quedan banderas y si ya no le quedan casillas sin minas
        if self.minas == 0 and self.casillas_abiertas == 0:
            self.after(10, self.terminarPartida)

    def mostrarZeros(self, ix, iy):
        """muestra todas las casillas vacias desde [ix][iy]"""
        derecha = False
        izquierda = False
        arriba = False
        abajo = False

        if ix+1 < self.x:
            derecha = True #revisar borde a la derecha
            self.matrix[iy][ix+1].bindButton()
        if 0 <= ix-1:
            izquierda = True #revisar borde a la izquierda
            self.matrix[iy][ix-1].bindButton()

        if 0 <= iy-1:
            arriba = True #revisar borde de arriba
            self.matrix[iy-1][ix].bindButton()
            
        if iy+1 < self.y:
            abajo = True #revisar borde de abajo
            self.matrix[iy+1][ix].bindButton()

        if arriba and derecha:
            self.matrix[iy-1][ix+1].bindButton()
        if arriba and izquierda:
            self.matrix[iy-1][ix-1].bindButton()
                        
        if abajo and derecha:
            self.matrix[iy+1][ix+1].bindButton()
        if abajo and izquierda:
            self.matrix[iy+1][ix-1].bindButton()

    def mostrarZerosAft(self, x, y):
        self.after(10, lambda: self.mostrarZeros(x, y))





if __name__ == "__main__":
    ven = tk.Tk()
    # ven.geometry("500x500")
    fr = tk.Frame(ven)
    fr.pack()

    mapa = Mapa(ven, ven.destroy, ven.destroy, print, 15, 15, .3)

    b1 = tk.Button(fr, text='reset', command=mapa.generar)
    b1.pack(side='left')

    b2 = tk.Button(fr, text='principiante', command=lambda: mapa.generar(10, 10, .3))
    b2.pack(side='left')

    b3 = tk.Button(fr, text='Intermedio', command=lambda: mapa.generar(16, 16, .5))
    b3.pack(side='left')

    b4 = tk.Button(fr, text='prueba', command=lambda: mapa.generar(20, 20, 20))
    b4.pack(side='left')

    ven.mainloop()
