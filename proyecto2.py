

#######################################
######## VERSION PYTHON 3.9.2 #########
#######################################
#Info programa principal
"""
Costa Rica
Instituto Tecnológico de Costa Rica
Área Académica de Ingeniería en Computadores
Taller de Programación, 2021, Grupo 2
Milton Villegas Lemus
Version Python 3.9.2
Versión del codigo 1.0
Editor: Geovanny García Downing, 2020092224
Entradas: no aplica
Salidas: ventana en ciclo TK
Restricciones: no aplica
Modulos usados: guardar_archivo, leer_archivo, close, cargar_imagen, cargarMP3, reprod_FX, detener_cancion, reprod_cancion, reproducir_salida, limitador, Vnivel1Check, Vnivel2Check, Vnivel3Check, checkPoints, mensajePuntos, cronom, reset_time, pause_time, Vnivel1, Vnivel2, Vnivel3, info_adicional, mejores_puntajes, autodocumentacion
Modulos modificados: Se reutilizó código de la tarea, cargar_imagen, abarcado por José Fernando Morales en el taller
Codigo modificado facilitado por: Jose Fernando Morales
"""
#Importacion de las funciones necesarias para el proyecto
from tkinter import *
from os import path
from time import *
from pygame import mixer
from pygame.constants import USEREVENT
from random import *
from threading import Thread
import glob

#Creación de las 3 fuentes más utilizadas en el proyecto, para mayor facilidad
fnt=("Candara Light",20)
fnt2=("Candara Light",12)
fnt3=("Candara Light",16)

#Variables de tiempo (horas , minutos, sgundos, FLAG)
timeFlag=0 #FLAG tiempo (proceso de cambio de Label)
h=0 
m=0
s=0

#Creación de FLAGS para disparar, mover nave y señal de keyrelease
shootFlag=True
moveFlag=False
keyFlag=True
FLAG=True

#Texto de la  ventana de información adicional
about="""
Costa Rica
Instituto Tecnológico de Costa Rica
Área Académica de Ingeniería en Computadores
Taller de Programación, 2021, Grupo 2
Milton Villegas Lemus
Versión 1.0
Geovanny García Downing
"""
#Listas que contienen puntajes y nombres del top 5 puntajes
puntajes=[]
nombres=[]

def guardar_archivo(archivo, i=0): #Función para guardar archivo de texto
    global nombres, puntajes
    try:
        archivo.write(nombres[i]+(str(puntajes[i]).zfill(2))+"\n") #guarda nombrepuntaje en cada linea de texto, los últimos 2 caractéres son números
        guardar_archivo(archivo,i+1)
    except:
        archivo.close()
        
def leer_archivo(archivo, i=1): #Función para leer el archrivo de texto con puntajes y nombre
    global nombres, puntajes
    try:
        line=archivo.readline() #toma los últimos 2 digitos de cada line y los toma como el puntaje, el resto es el nombre
        puntajes.append(int(line[-3:]))
        nombres.append(line[:-3])
        leer_archivo(archivo, i+1)
    except:
        archivo.close()
try:
    archivo=open("puntajes.txt","r+") #apertura de archivo en caso de existir
except:
    archivo=open("puntajes.txt","w+") #apertura de archivo en caso de no existir
leer_archivo(archivo)

ventana=Tk() #Creación de ventana y tamaño
ventana.title("WARTEC")
ventana.minsize(600,800) 
ventana.resizable(width=NO, height=NO) 
##############################################################################################################
                                             # Clase Niveles #
##############################################################################################################

class Meteor:
    canvas=0
    def __init__(self, canvas, imagen):
        self.canvas=canvas
        self.imagen=imagen
    
    def obstaculo(self):
        def create_space(canva,imagen) : #crea un meteor
            space = canva.create_image(randint(50,450),randint(100,650),anchor=NW, image=imagen, tags="meteorito")
            return space
        def movimiento(meteor):
            x0 = self.canvas.coords(meteor)[0]
            y0 = self.canvas.coords(meteor)[1]
            speed_x = choice([1,-1])
            speed_y = choice([1,-1])
            while FLAG:
                self.canvas.move(meteor, speed_x, speed_y)
                sleep(0.007)
                if x0 >= 500:
                    speed_x = -1
                if x0 <= 0:
                    speed_x = 1
                if y0 >= 700:
                    speed_y = -1
                if y0 <= 0:
                    speed_y = 1
                x0 += speed_x
                y0 += speed_y
        Thread(target=movimiento, args=(create_space(self.canvas, self.imagen),)).start()
           
class Niveles:
    music=""
    fondo=""
    canvas=0
    def __init__(self,music,fondo,canvas=0):
        self.music=music
        self.fondo=fondo
        self.canvas=canvas
    
    def basico(self):
        global FLAG
        FLAG=True
        pts=0
        life=50
        ventana.withdraw() #oculta ventana principal
        nivel1=Toplevel() 
        nivel1.title("Nivel 1") 
        nivel1.minsize(600,800)
        nivel1.resizable(width=NO, height=NO)
        reprod_cancion(self.music)

        def end(): #función que calcula los bonuses en caso de finalizar, no hay bonuses en cierres forzados
            global ventana, h, m, s, FLAG
            nonlocal pts, nombre, life
            FLAG=False
            if life==50: #si la vida es 50 entonces se obtiene +10 bonus
                pts+=10
            if h==0 and m==0 and s<=30: #si lo hizo en 30 segs +20 bonus
                pts+=20
            reset_time()
            checkPoints(pts, nombre, 0)
            detener_cancion()
            ventana.deiconify() #reaparece la ventana principal
            nivel1.destroy() #cierra la subventana nivel1
            reprod_cancion("assets\\title.mp3")

        def back(): #función del botón BACK
            global ventana, FLAG
            nonlocal pts, nombre
            FLAG=False
            reset_time()
            checkPoints(pts, nombre, 0)
            detener_cancion()
            ventana.deiconify() #reaparece la ventana principal
            nivel1.destroy() #cierra la subventana nivel1
            reprod_cancion("assets\\title.mp3")

        def close(): #función de cierre
            nonlocal nivel1
            global ventana, FLAG
            FLAG=False #da la señal para detener animación
            detener_cancion()
            reproducir_salida() #reproduce efecto de salida
            sleep(0.9) #tiempo de ejecución del efecto
            nivel1.destroy() #cierra suventana y luego ventana
            ventana.destroy()

        #Creación canvas del nivel1 
        C_nivel1=Canvas(nivel1, width=600, height=800)
        self.canvas=C_nivel1
        C_nivel1.place(x=0,y=0)

        #Asiganción fondo subventana
        C_nivel1.fondoT=cargar_img(self.fondo)
        fondoT = C_nivel1.create_image(0,0,anchor=NW, image=C_nivel1.fondoT)

        #Creación del botón BACK
        C_app.back=cargar_img("back.png") #carga imagen para elbotón
        Btn_back=Button(C_nivel1, text='saludar',image=C_app.back, font=fnt, command=back)
        Btn_back.place(x=600,y=0, anchor=NE)

        #obtiene el nombre del entry
        nombre=E_nombre.get()

        #Labels con info del jugador
        Label_nombre=Label(C_nivel1, font=fnt3, bg="#850458", fg="#ffffff", text=nombre+"'s score: "+str(pts)+" pts")
        Label_nombre.place(x=0,y=0,anchor=NW)

        Label_life=Label(C_nivel1, font=fnt3, bg="#850458", fg="#ffffff", text=nombre+"'s life: "+str(life)+" pts")
        Label_life.place(x=0,y=50,anchor=NW)

        Label_time=Label(C_nivel1, font=fnt3, bg="#850458", fg="#ffffff")
        Label_time.place(x=600,y=50,anchor=NE)
        cronom(Label_time)#llamada al cronómetro
                
        def colision(x1,y1,w1,h1,x2,y2,w2,h2): #verifica colisiones mediante comparaciones de rangos en un área coordenadas, ancho y alto
            if x1>x2+w2 or x1+w1<x2 or y1>y2+h2 or y1+h1<y2:
                return False
            else:
                return True
        
        def animar(id, patron):
            imagen = cargarSprites(patron)
            Thread(target = moverSprite, args=(0, id, imagen)).start()

        def cargarSprites(patron): #cargar las imagenes que forman la animacion
            frame_ruta = glob.glob('assets/sprite/'+ patron) #ruta de frame 
            frame_ruta.sort() # ordenar las imagenes
            return cargarVarios(frame_ruta, []) #retormo de una lista con las rutas de frames

        def cargarVarios( list_img, listaResultado):
            if list_img == []: #condición de terminación
                return listaResultado 
            else:
                listaResultado.append(PhotoImage(file = list_img[0])) 
                return cargarVarios(list_img[1:], listaResultado) # llamada recursiva 

        def moverSprite(i, id, lista):
            if i == 6 : #condición para continuar con la secuencia de imagenes 
                i = 0
            C_nivel1.itemconfig(id, image = lista[i]) #cambiar las imagenes dentro del canvas y en elemento imagen
            def callback():  #funcion recursiva
                moverSprite(i+1, id, lista)
            C_nivel1.after(100,callback)   #llamada recursiva

        #carga el ship y el ship dañado y los agrega a una lista
        ship=C_nivel1.create_image(300,750,anchor=NW, tags="ship")
        shipco=C_nivel1.coords(ship)
        animar(ship,"tile*.png")
        """
        def laser_mov(i,objeto,collFlag=True): #mueve el laser
            nonlocal C_nivel1, shipco, pts, Label_nombre, nombre
            lasco=C_nivel1.coords(objeto) #coordenadas en tiempo real
            if colision(lasco[0],lasco[1],50,89,bossco[0],bossco[1],175,175) and collFlag and bolife>0: #verifica colisión
                collFlag=False
                reprod_fx("hit2.mp3") #sonido de daño
                pts+=1
                Label_nombre["text"]=nombre+"'s score: "+str(pts)+" pts"
            if lasco[1]>-100:
                C_nivel1.move(objeto,0,i)
                def callback():
                    laser_mov(i-0.1 ,objeto,collFlag)
                C_nivel1.after(5 , callback)
            """       
        def smooth_mov(objeto,i,j): #cree este algoritmo para que el movimiento de la nave fuera más suave
            global moveFlag #bandera, produce movimiento hasta keyrelease
            m=C_nivel1.coords(objeto)
            if ((i==-1 and 550>m[0]) or (i==1 and m[0]>50) or (j==-1 and 751>m[1]) or (j==1 and m[1]>100)) and moveFlag:
                C_nivel1.move(objeto,-i,-j)
                def callback():
                    smooth_mov(objeto,i,j)
                C_nivel1.after(2, callback)

        def create_laser(canva,imagen) : #crea un laser cada vez que se dispara
            reprod_fx("metal.mp3") #sonido de disparo
            laser = canva.create_image(shipco[0],shipco[1],anchor="center", image=imagen)
            return #laser_mov(0,laser)

        def move_ship(evento):  #verifica lo que toca el usuario en el teclado
            nonlocal C_nivel1, shipco, ship
            global shootFlag, keyFlag, moveFlag
            if keyFlag:
                moveFlag=True #inicia movimiento hasta keyrelease
                if evento.keysym=="Left":
                    smooth_mov(ship,1,0)
                elif evento.keysym=="Right":
                    smooth_mov(ship,-1,0)
                elif evento.keysym=="Up":
                    smooth_mov(ship,0,1)
                elif evento.keysym=="Down":
                    smooth_mov(ship,0,-1)
                keyFlag=False #evita varias llamadas por estar presionado
            elif evento.keysym=="space":
                if shootFlag:
                    shipco=C_nivel1.coords(ship)
                    #create_laser(C_nivel1,C_nivel1.laser)
                    shootFlag=False #bloquea disparo presionado

        def stop_shoot(evento):
            global shootFlag, moveFlag, keyFlag #modifica ciertas banderas que dependen del keyreleas
            nonlocal life
            if evento.keysym=="space" and life>0:
                shootFlag=True #puede disparar luego de soltar mientras esté vivo
            else:
                moveFlag=False #deja de moverse
                keyFlag=True #se puede leer la presion de una tecla
        #eventos de press y release 
        nivel1.bind('<KeyPress>', move_ship)
        nivel1.bind('<KeyRelease>', stop_shoot)
        #cierre protocolo
        nivel1.protocol("WM_DELETE_WINDOW",close)
    
class Nivel1(Niveles):
    def __init__(self,music,fondo,canvas=0):
        Niveles.__init__(self,music,fondo,canvas)

    def create_meteor(self):
        self.canvas.meteorito=cargar_img("meteor.png")
        meteors=[Meteor(self.canvas,self.canvas.meteorito),Meteor(self.canvas,self.canvas.meteorito),Meteor(self.canvas,self.canvas.meteorito),Meteor(self.canvas,self.canvas.meteorito),Meteor(self.canvas,self.canvas.meteorito)]
        for i in meteors:
            i.obstaculo()
        

class Nivel2(Niveles):
    def __init__(self,music,fondo,canvas=0):
        Niveles.__init__(self,music,fondo,canvas)

class Nivel3(Niveles):
    def __init__(self,music,fondo,canvas=0):
        Niveles.__init__(self,music,fondo,canvas)

##############################################################################################################
                                             # Pantalla Principal #
##############################################################################################################

def close(): #función de cierre de la ventana principal
    global ventana 
    reproducir_salida() #reproduce el efecto Goodbye
    sleep(0.9) #tiempo para que se pueda reproducir el efecto
    ventana.destroy() 

def cargar_img(nombre):
    ruta=path.join("assets",nombre) #crea acceso a la ruta assets dentro de la carpeta del programa
    img=PhotoImage(file=ruta) #importa la imagen
    return img #retorna la imagen

C_app=Canvas(ventana, width=600, height=800) #creación del canvas de la ventana principal
C_app.place(x=0,y=0) 

C_app.fondo=cargar_img("fondo4.png") #se carga imagen para fondo
fondo = C_app.create_image(0,0,anchor=NW, image=C_app.fondo)

def reprod_fx(MP3):
    mixer.init()
    sound=mixer.Sound("assets/"+MP3)
    sound.play()

def detener_cancion(): #función para detener reproducción
    mixer.music.stop()

def reprod_cancion(MP3): #función para reproducir canción
    mixer.init()
    detener_cancion()
    playlist = []
    playlist.append (MP3)
    song=playlist.pop() 
    mixer.music.load (song)  
    mixer.music.queue (song)
    mixer.music.set_endevent (USEREVENT)   
    mixer.music.play(-1)
    
def reproducir_salida(): #función efecto de salida
    reprod_fx("goodbye.mp3")

L_about=Label(ventana, font=fnt, bg="#850458", fg="#ffffff", text="Ingrese su nombre")
L_about.place(x=300,y=150,anchor="center")

#Modificado del código de: Samuel Enrique Molina Bermudez
entry_text = StringVar() #string dinámico
E_nombre= Entry(ventana, width=14, font=fnt, textvariable = entry_text, justify=CENTER)
E_nombre.place(x=200,y=220,anchor="center")

def limitador(entry_text): #limita el texto a 12 caracteres
    if entry_text.get()!="":
        entry_text.set(entry_text.get()[:12])

entry_text.trace("w", lambda *args: limitador(entry_text))

def Vnivel1Check(): #check del box de nombre que no esté vacío y corre nivel 1
    if entry_text.get()=="":
        msgbox=Toplevel()
        msgbox.minsize(200,200)
        L_saludo=Label(msgbox,text="Debe ingresar un nombre",font=fnt2)
        L_saludo.place(x=100, y=100, anchor="center")
    else:
        Nivel01=Nivel1("assets\\nivel1.mp3","fondo1.png")
        Nivel01.basico()
        Nivel01.create_meteor()

def Vnivel2Check(): #check del box de nombre que no esté vacío y corre nivel 2
    if entry_text.get()=="":
        msgbox=Toplevel()
        msgbox.minsize(200,200)
        L_saludo=Label(msgbox,text="Debe ingresar un nombre",font=fnt2)
        L_saludo.place(x=100, y=100, anchor="center")
    else:
        Nivel02=Nivel2("assets\\nivel2.mp3","fondo2.png")
        Nivel02.basico()

def Vnivel3Check(): #check del box de nombre que no esté vacío y corre nivel 3
    if entry_text.get()=="":
        msgbox=Toplevel()
        msgbox.minsize(200,200)
        L_saludo=Label(msgbox,text="Debe ingresar un nombre",font=fnt2)
        L_saludo.place(x=100, y=100, anchor="center")
    else:
        Nivel03=Nivel3("assets\\nivel3.mp3","fondo3.png")
        Nivel03.basico()

def checkPoints(Pts, Nombre, I): #guarda el puntaje en la lista
    global puntajes, nombres
    if Pts>0:
        if puntajes!=[]: #si está vacía nada más agrega al final
            try: #si la lista se sale de rango
                puntajes[I]
                if puntajes[I]<=Pts: #compara cada valor con los puntos
                    puntajes=puntajes[:I]+[Pts]+puntajes[I:] #quiebra lista y mete en medio
                    nombres=nombres[:I]+[Nombre]+nombres[I:]
                    try:
                        puntajes[5] #en caso de agregar un extra espacio, se elimina, quedando sólo 5
                        puntajes=puntajes[:-1]
                    except:
                        pass
                    archivo=open("puntajes.txt","w+") #guarda en archivo
                    guardar_archivo(archivo)
                    reprod_fx("congratulations.mp3")
                    return mensajePuntos(Pts,I+1) #i+1 es la posición en la que el jugador quedó y llama a la función que envía mensaje a ganador de nuevo record
                else:
                    return checkPoints(Pts, Nombre, I+1) #llamada recursiva
            except: #si se sale de rango y el i es menor a 5 se agrega al final
                if I<5:
                    nombres+=[Nombre]
                    puntajes+=[Pts]
                    archivo=open("puntajes.txt","w+") #guarda archivo
                    guardar_archivo(archivo)
                    reprod_fx("congratulations.mp3")
                    return mensajePuntos(Pts,I+1) #llama a la función que envía mensaje a ganador de nuevo record
                else:
                    pass
        else:
            nombres+=[Nombre] #agrega al final en caso de vacía
            puntajes+=[Pts]
            archivo=open("puntajes.txt","w+") #guarda en archivo
            guardar_archivo(archivo)
            reprod_fx("congratulations.mp3")
            return mensajePuntos(Pts,I+1)

def mensajePuntos(Pts,Pos): #función que genera mensaje al ganador de nuevo record
    msgbox=Toplevel()
    msgbox.minsize(600,600)
    L_score=Label(msgbox,text=f"Usted se encuentra entre \nlos mejores puntajes,\nobtuvo la posición {Pos} \ncon {Pts} puntos",font=("Candara Light",24))
    L_score.place(x=300, y=300, anchor="center")

def cronom(Label): #función que genera el cronómetro
    global timeFlag, h, m, s
    #Verificamos si los segundos y los minutos son mayores a 60
    if s >= 60:
        s=0
        m+=1
        if m >= 60:
            m=0
            h+=1
    # iniciamos la cuenta progresiva de los segundos
    Label['text'] ="Time: "+str(h)+":"+str(m).zfill(2)+":"+str(s).zfill(2) #modifica dinámicamente el texto del label de tiempo
    s+=1
    timeFlag=Label.after(1000, cronom, (Label)) #llamada recursiva cada 1 segundo

def reset_time(): #resetea las variables de tiempo a 0
    global h, m, s
    h=0
    m=0
    s=0

def pause_time(Label): #pausa el cronómetro
    global timeFlag
    Label.after_cancel(timeFlag)

reprod_cancion("assets\\title.mp3") #reproduce musica de fondo con

##############################################################################################################
                                                # About #
##############################################################################################################
def info_adicional():
    """
    Costa Rica
    Instituto Tecnológico de Costa Rica
    Área Académica de Ingeniería en Computadores
    Taller de Programación, 2021, Grupo 2
    Milton Villegas Lemus
    Version Python 3.9.2
    Versión del codigo 1.0
    Editor: Geovanny García Downing, 2020092224
    Entradas: no aplica
    Salidas: ventana en ciclo TopLevel
    Restricciones: no aplica
    Modulos usados: back, close
    """
    global ventana, about
    ventana.withdraw() #oculta ventana principal
    info=Toplevel() #creción de subventana de información adicional y características por Toplevel
    info.title("Información Adicional")
    info.minsize(600,800)
    info.resizable(width=NO, height=NO)
    
    def back(): #función del botón BACK
        global ventana
        ventana.deiconify() #reaparece ventana principal
        info.destroy() #cierra ventana de info

    def close(): #función de cierre
        nonlocal info
        global ventana
        reproducir_salida() #reproduce efecto de salida Goodbye
        sleep(0.9) #tiempo de reproducción efecto
        info.destroy() #cierra subventana y luego ventana
        ventana.destroy()
    
    #Creación canvas de subventana Info   
    C_info=Canvas(info, width=600, height=800)
    C_info.place(x=0,y=0)

    #Asignación fondo de subventana Info
    C_info.fondoI=cargar_img("fondo1.png")
    fondoI = C_info.create_image(0,0,anchor=NW, image=C_info.fondoI)

    #Creación botón BACK
    C_app.back=cargar_img("back.png") #Carga imagen para botón
    Btn_back=Button(info, text='saludar',image=C_app.back, font=fnt, command=back)
    Btn_back.place(x=600,y=0, anchor=NE)

    #Label con el texto de info adicional (about)
    L_about=Label(info,font=fnt, bg="#ffffff", fg="#000000", text=about)
    L_about.place(x=300, y=380, anchor="center")

    info.protocol("WM_DELETE_WINDOW",close) 

##############################################################################################################
                                                # Puntajes #
##############################################################################################################
def mejores_puntajes():
    """
    Costa Rica
    Instituto Tecnológico de Costa Rica
    Área Académica de Ingeniería en Computadores
    Taller de Programación, 2021, Grupo 2
    Milton Villegas Lemus
    Version Python 3.9.2
    Versión del codigo 1.0
    Editor: Geovanny García Downing, 2020092224
    Entradas: no aplica
    Salidas: ventana en ciclo TopLevel
    Restricciones: no aplica
    Modulos usados: back, close, tablero,
    """
    global puntajes, nombres, ventana, about
    ventana.withdraw() #oculta ventana principal
    info=Toplevel() #creción de subventana de información adicional y características por Toplevel
    info.title("Información Adicional")
    info.minsize(600,800)
    info.resizable(width=NO, height=NO)
    
    def tablero(Puntajes,I): #retorna un texto con los puntajes, nombres y posiciones
        if Puntajes==[]:
            return ""
        else:
            return f"{I+1}. {nombres[I]} \t\t---> {Puntajes[0]}\n" + tablero(Puntajes[1:],I+1)

    def back(): #función del botón BACK
        global ventana
        ventana.deiconify() #reaparece ventana principal
        info.destroy() #cierra ventana de info

    def close(): #función de cierre
        nonlocal info
        global ventana
        reproducir_salida() #reproduce efecto de salida Goodbye
        sleep(0.9) #tiempo de reproducción efecto
        info.destroy() #cierra subventana y luego ventana
        ventana.destroy()
    
    #Creación canvas de subventana Info   
    C_info=Canvas(info, width=600, height=800)
    C_info.place(x=0,y=0)

    #Asignación fondo de subventana Info
    C_info.fondoI=cargar_img("fondo1.png")
    fondoI = C_info.create_image(0,0,anchor=NW, image=C_info.fondoI)

    #Creación botón BACK
    C_app.back=cargar_img("back.png") #Carga imagen para botón
    Btn_back=Button(info, text='saludar',image=C_app.back, font=fnt, command=back)
    Btn_back.place(x=600,y=0, anchor=NE)

    #Label con el texto de info adicional (about)
    L_about=Label(info,font=fnt, bg="#ffffff", fg="#000000", text=tablero(puntajes,0))
    L_about.place(x=300, y=380, anchor="center")

    info.protocol("WM_DELETE_WINDOW",close) 


Btn_jugar=Button(ventana, text='Jugar',font=fnt,command=Vnivel1Check, bg="#850458", fg="#ffffff")
Btn_jugar.place(x=400,y=220,anchor="center")    
    
#Creación botón para abrir subventana Nivel 1
Btn_nivel1=Button(ventana, text='Nivel 1',font=fnt,command=Vnivel1Check, bg="#850458", fg="#ffffff")
Btn_nivel1.place(x=300,y=320,anchor="center")

#Creación botón para abrir subventana Nivel 2
Btn_nivel2=Button(ventana, text='Nivel 2',font=fnt,command=Vnivel2Check, bg="#850458", fg="#ffffff")
Btn_nivel2.place(x=300,y=420,anchor="center")

#Creación botón para abrir subventana Nivel 3
Btn_nivel3=Button(ventana, text='Nivel 3',font=fnt,command=Vnivel3Check, bg="#850458", fg="#ffffff")
Btn_nivel3.place(x=300,y=520,anchor="center")

#Creación botón para abrir subventana Puntajes
#Btn_pt=Button(ventana, text='Mejores Puntajes',font=fnt,command=mejores_puntajes, bg="#850458", fg="#ffffff")
#Btn_pt.place(x=300,y=620,anchor="center")

#Creación botón para abrir subventana Información Adicional
#Btn_info=Button(ventana, text='Información Adicional',font=fnt,command=info_adicional, bg="#850458", fg="#ffffff")
#Btn_info.place(x=300,y=720,anchor="center")

ventana.protocol("WM_DELETE_WINDOW", close)
ventana.mainloop()