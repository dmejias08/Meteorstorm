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
Editores: Geovanny García Downing, 2020092224 y Diana Mejías Hernández, 2020077281
Entradas: no aplica
Salidas: ventana en ciclo TK
Restricciones: no aplica
Modulos usados: guardar_archivo, leer_archivo, close, cargar_imagen, cargarMP3, reprod_FX, detener_cancion, reprod_cancion, reproducir_salida, limitador, Vnivel1Check, Vnivel2Check, Vnivel3Check, checkPoints, mensajePuntos, cronom, reset_time, pause_time, Vnivel1, Vnivel2, Vnivel3, info_adicional, mejores_puntajes, autodocumentacion, insertion, quick, partir
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
meteors=[]

variable = "\\"

#Texto de la  ventana de información adicional
about="""
Costa Rica
Instituto Tecnológico de Costa Rica
Área Académica de Ingeniería en Computadores
Taller de Programación, 2021, Grupo 2
Milton Villegas Lemus
Versión 1.0
Geovanny García Downing
Diana Mejías Hernandez
"""
#Listas que contienen puntajes y nombres del top 5 puntajes
puntajes=[]
nombres=[]
shipco=[]

def guardar_archivo(archivo, i=0): #Función para guardar archivo de texto
    global puntajes
    try:
        archivo.write(puntajes[i][0]+(str(puntajes[i][1]).zfill(3))+"\n") #guarda nombrepuntaje en cada linea de texto, los últimos 2 caractéres son números
        guardar_archivo(archivo,i+1)
    except:
        archivo.close()
        
def leer_archivo(archivo, i=1): #Función para leer el archrivo de texto con puntajes y nombre
    global puntajes
    try:
        line=archivo.readline() #toma los últimos 2 digitos de cada line y los toma como el puntaje, el resto es el nombre
        puntajes.append([line[:-4],int(line[-4:])])
        leer_archivo(archivo, i+1)
    except:
        archivo.close()
try:
    archivo=open("puntajes.txt","r+") #apertura de archivo en caso de existir
except:
    archivo=open("puntajes.txt","w+") #apertura de archivo en caso de no existir
leer_archivo(archivo)

ventana=Tk() #Creación de ventana y tamaño
ventana.title("METEORSTORM")
ventana.minsize(600,800) 
ventana.resizable(width=NO, height=NO) 
##############################################################################################################
                                             # Clase Niveles #
##############################################################################################################

class Meteor: #Clase Meteorito 
    """
    Costa Rica
    Instituto Tecnológico de Costa Rica
    Área Académica de Ingeniería en Computadores
    Taller de Programación, 2021, Grupo 2
    Milton Villegas Lemus
    Version Python 3.9.2
    Versión del codigo 1.0
    Editores: Geovanny García Downing, 2020092224 y Diana Mejías Hernández, 2020077281
    Entradas: no aplica
    Salidas: ventana en ciclo TopLevel
    Restricciones: no aplica
    Modulos usados: getCoords, obstáculo, movimiento
    """
    def __init__(self, canvas, imagen, id):
        self.canvas=canvas
        self.imagen=imagen
        self.id=id
    def getCoords(self):
        print(self.coordi)

    def obstaculo(self): #Creacion del id para objeto meteorito 
        def create_space(canva,imagen) : #crea un meteor
            space = canva.create_image(randint(50,450),randint(100,550),anchor=NW, image=imagen, tags="meteorito")
            self.id=space
            return space
        def movimiento(meteor): #Toma objeto y lo mueve 
            global shipco
            x0 = self.canvas.coords(meteor)[0]
            y0 = self.canvas.coords(meteor)[1]
            speed_x = choice([1,-1])
            speed_y = choice([1,-1])
            while FLAG:
                try:
                    self.coordi=self.canvas.coords(meteor) #Actulizacion de coordenadas 
                    self.canvas.move(meteor, speed_x, speed_y)
                    sleep(0.006)
                    if x0 >= 500:
                        speed_x = -1
                        reprod_fx("thump.mp3")
                    if x0 <= 0:
                        speed_x = 1
                        reprod_fx("thump.mp3")
                    if y0 >= 700:
                        speed_y = -1
                        reprod_fx("thump.mp3")
                    if y0 <= 0:
                        speed_y = 1
                        reprod_fx("thump.mp3")
                    x0 += speed_x
                    y0 += speed_y
                except:
                    pass
        if meteors!=[]: #Verifica condicion de finalizacion 
            Thread(target=movimiento, args=(create_space(self.canvas, self.imagen),)).start() #Inicio de hilo movimiento 
           
class Niveles: #Inico de clase niveles
    """
    Costa Rica
    Instituto Tecnológico de Costa Rica
    Área Académica de Ingeniería en Computadores
    Taller de Programación, 2021, Grupo 2
    Milton Villegas Lemus
    Version Python 3.9.2
    Versión del codigo 1.0
    Editores: Geovanny García Downing, 2020092224 y Diana Mejías Hernández, 2020077281
    Entradas: no aplica
    Salidas: ventana en ciclo TopLevel
    Restricciones: no aplica
    Modulos usados: basico, back, backB, close, cronom, animar_exp, animar,cargarSprite, moverSprite, cargarVarios, exp_anim, checkLife, coll_ship. smooth_move, moveShip
    """ 
    music=""
    fondo=""
    canvas=0

    def __init__(self,music,fondo,canvas):
        self.music=music
        self.fondo=fondo
        self.canvas=canvas

    def basico(self):
        global FLAG, meteors
        FLAG=True
        notdead=True
        sprFlag=True
        reset_time()
        pts=0
        life=3
        ventana.withdraw() #oculta ventana principal
        nivel1=Toplevel() 
        nivel1.title("Nivel 1") 
        nivel1.minsize(600,800)
        nivel1.resizable(width=NO, height=NO)
        reprod_cancion(self.music)

        def backB():
            nonlocal pts, nombre, Label_time
            pause_time(Label_time)
            checkPoints(pts,nombre)
            back()

        def back(): #función del botón BACK
            global ventana, FLAG, meteors
            nonlocal pts, nombre, notdead, C_nivel1
            meteors=[]
            notdead=False
            FLAG=False
            reset_time()
            sleep(0.5)
            detener_cancion()
            ventana.deiconify() #reaparece la ventana principal
            nivel1.destroy() #cierra la subventana nivel1
            reprod_cancion("assets"+variable+"title.mp3")

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
        Btn_back=Button(C_nivel1, text='saludar',image=C_app.back, font=fnt, command=backB)
        Btn_back.place(x=600,y=0, anchor=NE)

        #obtiene el nombre del entry
        nombre=E_nombre.get()

        #Labels con info del jugador
        Label_nombre=Label(C_nivel1, font=fnt3, bg="#002663", fg="#ffffff", text=nombre+"'s score: "+str(pts)+" pts")
        Label_nombre.place(x=0,y=0,anchor=NW)

        Label_life=Label(C_nivel1, font=fnt3, bg="#002663", fg="#ffffff", text=nombre+"'s life: "+str(life)+" pts")
        Label_life.place(x=0,y=50,anchor=NW)

        Label_time=Label(C_nivel1, font=fnt3, bg="#002663", fg="#ffffff")
        Label_time.place(x=600,y=50,anchor=NE)
        
        def cronom(LabelT): #función que genera el cronómetro
            global timeFlag, h, m, s, meteors
            nonlocal pts, Label_nombre
            #Verificamos si los segundos y los minutos son mayores a 60
            if s == 60:
                pause_time(LabelT)
                msgbox=Toplevel() #mensaje de juego finalizado
                msgbox.minsize(600,600)
                L_saludo=Label(msgbox,text="JUEGO\nFINALIZADO\nGanó",font=("Candara Light",30))
                L_saludo.place(x=300, y=300, anchor="center")
                meteors=[]
                def fin(): #llama a la función end luego de 5 segundos
                    nonlocal msgbox
                    msgbox.destroy()
                    if self.fondo[-5]=="1":
                        checkPoints(60, nombre)
                    elif self.fondo[-5]=="2":
                        checkPoints(180, nombre)
                    elif self.fondo[-5]=="3":
                        checkPoints(300, nombre)
                    back()
                C_nivel1.after(5000,fin)

            # iniciamos la cuenta progresiva de los segundos
            LabelT['text'] ="Time: "+str(h)+":"+str(m).zfill(2)+":"+str(s).zfill(2) #modifica dinámicamente el texto del label de tiempo
            if self.fondo[-5]=="1":
                pts=s
            elif self.fondo[-5]=="2":
                pts=3*s
            elif self.fondo[-5]=="3":
                pts=5*s
            Label_nombre['text'] =nombre+"'s score: "+str(pts)+" pts"
            s+=1
            if s<=60:
                timeFlag=LabelT.after(1000, cronom, (LabelT)) #llamada recursiva cada 1 segundo
        
        cronom(Label_time)#llamada al cronómetro
        C_nivel1.damage=cargar_img("damage1.png")
                
        def colision(x1,y1,w1,h1,x2,y2,w2,h2): #verifica colisiones mediante comparaciones de rangos en un área coordenadas, ancho y alto
            if x1>x2+w2 or x1+w1<x2 or y1>y2+h2 or y1+h1<y2:
                return False
            else:
                return True
        
        def animar(id, patron,ruta):
            imagen = cargarSprites(patron,ruta)
            Thread(target = moverSprite, args=(0, id, imagen)).start()

        def animar_exp(id, patron,ruta):
            if life>0:
                imagen = cargarSprites(patron,ruta)
                Thread(target = exp_anim, args=(0, id, imagen)).start()

        def cargarSprites(patron,ruta): #cargar las imagenes que forman la animacion
            frame_ruta = glob.glob(ruta+ patron) #ruta de frame 
            frame_ruta.sort() # ordenar las imagenes
            return cargarVarios(frame_ruta, []) #retormo de una lista con las rutas de frames

        def cargarVarios( list_img, listaResultado):
            if list_img == []: #condición de terminación
                return listaResultado 
            else:
                listaResultado.append(PhotoImage(file = list_img[0])) 
                return cargarVarios(list_img[1:], listaResultado) # llamada recursiva 

        def moverSprite(i, id, lista):
            nonlocal sprFlag, notdead
            if i == 6 : #condición para continuar con la secuencia de imagenes 
                i = 0
            def callback():  #funcion recursiva
                moverSprite(i+1, id, lista)
            if sprFlag and notdead:
                C_nivel1.itemconfig(id, image = lista[i]) #cambiar las imagenes dentro del canvas y en elemento imagen
                C_nivel1.after(100,callback)   #llamada recursiva
            elif sprFlag==False and notdead:
                C_nivel1.itemconfig(id, image = C_nivel1.damage)
                C_nivel1.after(500,callback)   #llamada recursiva 

        def exp_anim(i, id, lista):
            nonlocal sprFlag, notdead
            if i == 33 : #condición para continuar con la secuencia de imagenes 
                C_nivel1.delete(id)
                return
            def callback():  #funcion recursiva
                exp_anim(i+1, id, lista)
            C_nivel1.itemconfig(id, image = lista[i]) #cambiar las imagenes dentro del canvas y en elemento imagen
            if notdead:
                C_nivel1.after(25,callback)   #llamada recursiva

        #carga el ship y el ship dañado y los agrega a una lista
        ship=C_nivel1.create_image(300,700,anchor=NW, tags="ship")
        shipco=C_nivel1.coords(ship)
        animar(ship,"tile*.png",'assets/sprite/')
        C_nivel1.laser=cargar_img("laser.png")

        def checklife():
            nonlocal notdead, life
            if life==0 and notdead:
                notdead=False
                pause_time(Label_time) #pausa tiempo
                msgbox=Toplevel() #mensaje de juego finalizado
                msgbox.minsize(600,600)
                L_saludo=Label(msgbox,text="JUEGO\nFINALIZADO\nPerdió",font=("Candara Light",30))
                L_saludo.place(x=300, y=300, anchor="center")
                def fin(): #llama a la función end luego de 5 segundos
                    nonlocal msgbox
                    msgbox.destroy()
                    checkPoints(pts,nombre)
                    back()
                C_nivel1.after(5000,fin)

        def coll_ship():
            nonlocal C_nivel1, shipco, life, Label_nombre, nombre, sprFlag, notdead
            global meteors
            shipco=C_nivel1.coords(ship) #coordenadas en tiempo real
            if notdead:
                for j in meteors:
                    bossco=C_nivel1.coords(j.id)
                    if colision(shipco[0],shipco[1],75,75,bossco[0],bossco[1],75,75) and life>0: #verifica colisión
                        reprod_fx("explo4.mp3") #sonido de daño
                        life-=1
                        Label_life["text"]=nombre+"'s life: "+str(life)+" pts"
                        sprFlag=False #cambia a nave dañada
                        def normal(): #vuelve a nave normal después de medio segundo
                            nonlocal C_nivel1,sprFlag
                            sprFlag=True
                        C_nivel1.after(500,normal)
                        exp=C_nivel1.create_image(bossco[0],bossco[1],anchor=NW, tags="exp")
                        animar_exp(exp,"tile**.png","assets/explosion/")
                        C_nivel1.delete(j.id)
                        meteors.remove(j)
                        if checklife():
                            back()
                            return
                def callback():
                    coll_ship()
                C_nivel1.after(5 , callback)
                   
        def smooth_mov(objeto,i,j): #cree este algoritmo para que el movimiento de la nave fuera más suave
            global moveFlag, shipco #bandera, produce movimiento hasta keyrelease
            nonlocal notdead
            shipco=C_nivel1.coords(objeto)
            if ((i==-1 and 500>shipco[0]) or (i==1 and shipco[0]>0) or (j==-1 and 700>shipco[1]) or (j==1 and shipco[1]>100)) and moveFlag and notdead:
                C_nivel1.move(objeto,-i,-j)
                def callback():
                    smooth_mov(objeto,i,j)
                C_nivel1.after(1, callback)

        def move_ship(evento):  #verifica lo que toca el usuario en el teclado
            nonlocal C_nivel1, shipco, ship, notdead
            global shootFlag, keyFlag, moveFlag
            if keyFlag and notdead:
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

        def stop_shoot(evento):
            global shootFlag, moveFlag, keyFlag #modifica ciertas banderas que dependen del keyreleas
            nonlocal life
            if evento.keysym=="space" and life>0:
                shootFlag=True #puede disparar luego de soltar mientras esté vivo
            else:
                moveFlag=False #deja de moverse
                keyFlag=True #se puede leer la presion de una tecla

        coll_ship()
        #eventos de press y release 
        nivel1.bind('<KeyPress>', move_ship)
        nivel1.bind('<KeyRelease>', stop_shoot)
        #cierre protocolo
        nivel1.protocol("WM_DELETE_WINDOW",close)

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

L_about=Label(ventana, font=fnt, bg="#002663", fg="#ffffff", text="Ingrese su nombre")
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
    """
    Costa Rica
    Instituto Tecnológico de Costa Rica
    Área Académica de Ingeniería en Computadores
    Taller de Programación, 2021, Grupo 2
    Milton Villegas Lemus
    Version Python 3.9.2
    Versión del codigo 1.0
    Editores: Geovanny García Downing, 2020092224 y Diana Mejías Hernández, 2020077281
    Entradas: no aplica
    Salidas: ventana en ciclo TopLevel
    Restricciones: no aplica
    Modulos usados: movimiento, obstáculo, básico
    """
    global meteors
    if entry_text.get()=="":
        msgbox=Toplevel()
        msgbox.minsize(200,200)
        L_saludo=Label(msgbox,text="Debe ingresar un nombre",font=fnt2)
        L_saludo.place(x=100, y=100, anchor="center")
    else:
        Nivel01=Niveles("assets"+variable+"nivel1.mp3","fondo1.png",0)
        Nivel01.basico()
        Nivel01.canvas.meteorito=cargar_img("meteor.png")
        im=Nivel01.canvas.meteorito
        ca=Nivel01.canvas
        meteors=[Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0)]
        for i in meteors:
            i.obstaculo()
        

def Vnivel2Check(): #check del box de nombre que no esté vacío y corre nivel 2
    """
    Costa Rica
    Instituto Tecnológico de Costa Rica
    Área Académica de Ingeniería en Computadores
    Taller de Programación, 2021, Grupo 2
    Milton Villegas Lemus
    Version Python 3.9.2
    Versión del codigo 1.0
    Editores: Geovanny García Downing, 2020092224 y Diana Mejías Hernández, 2020077281
    Entradas: no aplica
    Salidas: ventana en ciclo TopLevel
    Restricciones: no aplica
    Modulos usados: movimiento, obstáculo, básico
    """
    global meteors
    if entry_text.get()=="":
        msgbox=Toplevel()
        msgbox.minsize(200,200)
        L_saludo=Label(msgbox,text="Debe ingresar un nombre",font=fnt2)
        L_saludo.place(x=100, y=100, anchor="center")
    else:
        Nivel02=Niveles("assets"+variable+"nivel2.mp3","fondo2.png",0)
        Nivel02.basico()
        Nivel02.canvas.meteorito=cargar_img("meteor.png")
        im=Nivel02.canvas.meteorito
        ca=Nivel02.canvas
        meteors=[Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0)]
        for i in meteors:
            i.obstaculo()

def Vnivel3Check(): #check del box de nombre que no esté vacío y corre nivel 3
    """
    Costa Rica
    Instituto Tecnológico de Costa Rica
    Área Académica de Ingeniería en Computadores
    Taller de Programación, 2021, Grupo 2
    Milton Villegas Lemus
    Version Python 3.9.2
    Versión del codigo 1.0
    Editores: Geovanny García Downing, 2020092224 y Diana Mejías Hernández, 2020077281
    Entradas: no aplica
    Salidas: ventana en ciclo TopLevel
    Restricciones: no aplica
    Modulos usados: movimiento, obstáculo, básico
    """
    global meteors
    if entry_text.get()=="":
        msgbox=Toplevel()
        msgbox.minsize(200,200)
        L_saludo=Label(msgbox,text="Debe ingresar un nombre",font=fnt2)
        L_saludo.place(x=100, y=100, anchor="center")
    else:
        Nivel03=Niveles("assets"+variable+"nivel3.mp3","fondo3.png",0)
        Nivel03.basico()
        Nivel03.canvas.meteorito=cargar_img("meteor.png")
        im=Nivel03.canvas.meteorito
        ca=Nivel03.canvas
        meteors=[Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0),Meteor(ca,im,0)]
        for i in meteors:
            i.obstaculo()

def checkPoints(Pts, Nombre): #guarda el puntaje en la lista
    global puntajes, archivo
    puntajes.append([Nombre,Pts])
    listaN=quick(puntajes)
    if len(listaN)>=11:
        listaN=listaN[1:];
    if listaN!=puntajes or len(listaN)<=10:
        pos=0
        reprod_fx("congratulations.mp3")
        for i in range(1,len(listaN)+1):
            if listaN[-i]==[Nombre,Pts]:
                pos=i
        if pos!=0:
            mensajePuntos(Pts,pos)
    puntajes=listaN
    archivo=open("puntajes.txt","w+") #guarda en archivo
    guardar_archivo(archivo)

def quick(Lista):
    menores=[]
    iguales=[]
    mayores=[]
    if len(Lista)<=1:
        return Lista
    pivote=Lista[-1]
    partir(Lista,0,len(Lista),pivote,menores,iguales,mayores)
    ret=quick(menores)
    ret.extend(iguales)
    ret.extend(quick(mayores))
    return ret

def partir(Lista,i,n,Pivote,Menores,Iguales,Mayores):
    if i==n:
        return Menores,Iguales,Mayores
    if Lista[i][1]<Pivote[1]:
        Menores.append(Lista[i])
    elif Lista[i][1]>Pivote[1]:
        Mayores.append(Lista[i])
    elif Lista[i][1]==Pivote[1]:
        Iguales.append(Lista[i])
    return partir(Lista,i+1,n,Pivote,Menores,Iguales,Mayores)

def insertion(Lista):
    return insertion_aux(Lista,1,len(Lista))

def insertion_aux(Lista,i,n):
    if i==n:
        return Lista
    Aux=Lista[i]
    j=incluye_orden(Lista,i,Aux[0].lower())
    Lista[j]=Aux
    return insertion_aux(Lista,i+1,n)

def incluye_orden(Lista,j,Aux):
    if j<=0 or Lista[j-1][0]<=Aux:
        return j
    Lista[j]=Lista[j-1]
    return incluye_orden(Lista,j-1,Aux)
    
def mensajePuntos(Pts,Pos): #función que genera mensaje al ganador de nuevo record
    msgbox=Toplevel()
    msgbox.minsize(600,600)
    L_score=Label(msgbox,text=f"Usted se encuentra entre \nlos mejores puntajes,\nobtuvo la posición {Pos} \ncon {Pts} puntos",font=("Candara Light",24))
    L_score.place(x=300, y=300, anchor="center")

def reset_time(): #resetea las variables de tiempo a 0
    global h, m, s
    h=0
    m=0
    s=0

def pause_time(Label): #pausa el cronómetro
    global timeFlag
    Label.after_cancel(timeFlag)

reprod_cancion("assets"+variable+"title.mp3") #reproduce musica de fondo con

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
    Editores: Geovanny García Downing, 2020092224 y Diana Mejías Hernández, 2020077281
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
    C_info.fondoI=cargar_img("fondo4.png")
    fondoI = C_info.create_image(0,0,anchor=NW, image=C_info.fondoI)

    #Creación botón BACK
    C_app.back=cargar_img("back.png") #Carga imagen para botón
    Btn_back=Button(info, text='saludar',image=C_app.back, font=fnt, command=back)
    Btn_back.place(x=600,y=0, anchor=NE)

    #Label con el texto de info adicional (about)
    L_about=Label(info,font=fnt, bg="#ffffff", fg="#000000", text=about)
    L_about.place(x=300, y=380, anchor="center")

    C_info.geo=cargar_img("geo.png")
    geoF = C_info.create_image(150,700,anchor="center", image=C_info.geo)

    C_info.dian=cargar_img("dian.png")
    dianF = C_info.create_image(450,700,anchor="center", image=C_info.dian)

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
    Editores: Geovanny García Downing, 2020092224 y Diana Mejías Hernández, 2020077281
    Entradas: no aplica
    Salidas: ventana en ciclo TopLevel
    Restricciones: no aplica
    Modulos usados: back, close, tablero1, tablero2, tableroInsertion, tableroQuick
    """
    global puntajes, ventana, about
    ventana.withdraw() #oculta ventana principal
    info=Toplevel() #creción de subventana de información adicional y características por Toplevel
    info.title("Información Adicional")
    info.minsize(600,800)
    info.resizable(width=NO, height=NO)
    
    def tableroQuick():
        msgbox=Toplevel() #mensaje de PUNTAJES POR ORDEN NUMÉRICO
        msgbox.minsize(600,600)
        L_saludo=Label(msgbox,text=tablero1(puntajes,len(puntajes)-1),font=fnt)
        L_saludo.place(x=300, y=300, anchor="center")

    def tableroInsertion():
        msgbox=Toplevel() #mensaje de PUNTAJES POR ORDEN ALFABÉTICO
        msgbox.minsize(600,600)
        L_saludo=Label(msgbox,text=tablero2(insertion(puntajes),0),font=fnt)
        L_saludo.place(x=300, y=300, anchor="center")
    
    def tablero1(Puntajes,I): #retorna un texto con los puntajes, nombres y posiciones
        try:
            if I==-1:
                return ""
            else:
                return f"{len(Puntajes)-I}. {Puntajes[I][0]} \t\t---> {Puntajes[I][1]}\n" + tablero1(Puntajes,I-1)
        except:
            return ""

    def tablero2(Puntajes,I): #retorna un texto con los puntajes, nombres y posiciones
        try:
            if I==len(Puntajes):
                return ""
            else:
                return f"{I+1}. {Puntajes[I][0]} \t\t---> {Puntajes[I][1]}\n" + tablero2(Puntajes,I+1)
        except:
            return ""

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
    C_info.fondoI=cargar_img("fondo4.png")
    fondoI = C_info.create_image(0,0,anchor=NW, image=C_info.fondoI)

    #Creación botón BACK
    C_app.back=cargar_img("back.png") #Carga imagen para botón
    Btn_back=Button(info, text='saludar',image=C_app.back, font=fnt, command=back)
    Btn_back.place(x=600,y=0, anchor=NE)

    #Creación botón Quick Sort
    Btn_quick=Button(info, text='Quick Sort',font=fnt,command=tableroQuick, bg="#002663", fg="#ffffff")
    Btn_quick.place(x=300,y=270,anchor="center")

    #Creación botón Insertion Sort
    Btn_insert=Button(info, text='Insertion Sort',font=fnt,command=tableroInsertion, bg="#002663", fg="#ffffff")
    Btn_insert.place(x=300,y=540,anchor="center")

    #Label con el texto de info adicional (about)
    #L_about=Label(info,font=fnt, bg="#ffffff", fg="#000000", text=tablero(puntajes,len(puntajes)-1))
    #L_about.place(x=300, y=380, anchor="center")

    info.protocol("WM_DELETE_WINDOW",close) 


Btn_jugar=Button(ventana, text='Jugar',font=fnt,command=Vnivel1Check, bg="#002663", fg="#ffffff")
Btn_jugar.place(x=400,y=220,anchor="center")    
    
#Creación botón para abrir subventana Nivel 1
Btn_nivel1=Button(ventana, text='Nivel 1',font=fnt,command=Vnivel1Check, bg="#002663", fg="#ffffff")
Btn_nivel1.place(x=300,y=320,anchor="center")

#Creación botón para abrir subventana Nivel 2
Btn_nivel2=Button(ventana, text='Nivel 2',font=fnt,command=Vnivel2Check, bg="#002663", fg="#ffffff")
Btn_nivel2.place(x=300,y=420,anchor="center")

#Creación botón para abrir subventana Nivel 3
Btn_nivel3=Button(ventana, text='Nivel 3',font=fnt,command=Vnivel3Check, bg="#002663", fg="#ffffff")
Btn_nivel3.place(x=300,y=520,anchor="center")

#Creación botón para abrir subventana Puntajes
Btn_pt=Button(ventana, text='Mejores Puntajes',font=fnt,command=mejores_puntajes, bg="#002663", fg="#ffffff")
Btn_pt.place(x=300,y=620,anchor="center")

#Creación botón para abrir subventana Información Adicional
Btn_info=Button(ventana, text='Información Adicional',font=fnt,command=info_adicional, bg="#002663", fg="#ffffff")
Btn_info.place(x=300,y=720,anchor="center")

ventana.protocol("WM_DELETE_WINDOW", close)
ventana.mainloop()

def autodocumentacion():
    print("Niveles")
    print(Niveles.__doc__)
    print("Meteoritos")
    print(Meteor.__doc__)
    print("Check Nivel 1")
    print(Vnivel1Check.__doc__)
    print("Check Nivel 2")
    print(Vnivel2Check.__doc__)
    print("Check Nivel 3")
    print(Vnivel3Check.__doc__)
    print("Puntajes")
    print(mejores_puntajes.__doc__)
    print("About")
    print(info_adicional.__doc__)

autodocumentacion()

