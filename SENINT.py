try:                                                                      #
    from tkinter import *                                                 #
except ImportError:                                                       #
    print("Se requiere el modulo tkinter *")  


import os

try:                                                                      #
    import time                                                           #
except ImportError:                                                       #
    print("Se requiere el modulo time")  


try:                                                                      #
    from threading import Thread                                          #
except ImportError:                                                       #
    print("Se requiere el modulo threading")
    
    

from properties import *
from sensor import *
from controlPines import *


############################### centrar ventana #################################################################
                                                                                                                #
# https://stackoverflow.com/questions/36050192/how-to-position-toplevel-widget-relative-to-root-window          #                                                               
class centrarVentana:                                                                                           #
    def __init__(self, parent):                                                                                 #
        self.parent = parent                                                                                    #
        self.parent.update_idletasks()                                                                          #
        w = self.parent.winfo_screenwidth()                                                                     #
        h = self.parent.winfo_screenheight()                                                                    #
        size = tuple(int(_) for _ in self.parent.geometry().split('+')[0].split('x'))                           #
        x = w / 2 - size[0] / 2                                                                                 #
        y = h / 2 - size[1] / 2                                                                                 #
        self.parent.geometry("%dx%d+%d+%d" % (size + (x, y)))                                                   #
                                                                                                                #
#################################################################################################################  


################################################# utilidades ##################################################
                                                                                                              #
class util:                                                                                                   #
    def __init__(self, parent):                                                                               #
        self.parent = parent                                                                                  #
                                                                                                              #
    def mensajeAutoDestroid(self, texto="Probando..."):                                                       #
        self.top = Toplevel()                                                                                 #
        self.top.title('Capercio')                                                                            #
        self.top.geometry("650" + "x" + "70")                                                                 #
        Message(self.top, text=texto, padx=20, pady=20, font=("Helvetica", 16), width=600).pack()             #
        centrarVentana(self.top)                                                                              #
        self.top.after(6000, self.top.destroy)                                                                #
                                                                                                              #
    def progressbarAutoDestroid(self, texto="Probando...", tiempo=10000):                                     #
        self.topProgressbar = Toplevel()                                                                      #
        self.topProgressbar.title('Capercio')                                                                 #
        # top.wm_attributes('-alpha', 0.3)                                                                    #
        self.topProgressbar.geometry("620" + "x" + "50")                                                      #
        pbar_ind = ttk.Progressbar(self.topProgressbar, orient="horizontal", length=620, mode="indeterminate")#
        pbar_ind.grid(row=1, column=0, pady=2, padx=2, sticky=E + W + N + S)                                  #
        pbar_ind.start()                                                                                      #
        Label(self.topProgressbar, text=texto, font="Helvetica 16 bold italic").grid(row=0, column=0)         #
        centrarVentana(self.topProgressbar)                                                                   #
        self.topProgressbar.after(tiempo, self.topProgressbar.destroy)                                        #    
                                                                                                              #                                                                                                             #
###############################################################################################################


class MyDialog:
    def __init__(self, parent):
        self.top = Toplevel(parent)
        self.parent = parent
        self.top.title("Salir")
        Label(self.top, text="¿Está seguro?", font = "Helvetica 12 bold").grid(row=0, column=0, columnspan=2)
        self.button1 = Button(self.top, text="Si, salir de la app.", font = "Helvetica 12 bold", command=self.salir)
        self.button2 = Button(self.top, text="No, solo minimizar.", font = "Helvetica 12 bold", command=self.minimizar)
        self.button1.grid(row=1, column=0, padx=5, pady=5)
        self.button2.grid(row=1, column=1, padx=5, pady=5)              
        centrarVentana(self.top)

    def salir(self):
        self.top.destroy()
        self.parent.destroy()

    def minimizar(self):
        self.top.destroy()
        self.parent.iconify()
        time.sleep(3)
        self.parent.deiconify()





class ReiniciarSistema:
    def __init__(self, parent):
        self.top = Toplevel(parent)
        self.parent = parent
        self.top.title("Reiniciar")
        Label(self.top, text="No se encontró la imagen en el servidor para cargar en la aplicación,\npor favor reinicie el dispositivo para actualizar.", font = "Helvetica 12 italic").grid(row=0, column=0, columnspan=2)
        Label(self.top, text="¿Desea Reiniciar?", font = "Helvetica 12").grid(row=1, column=0, columnspan=2)
        self.button1 = Button(self.top, text="Si, Reiniciar el dispositivo.", font = "Helvetica 12 bold", command=self.reiniciar)
        self.button2 = Button(self.top, text="No, solo minimizar.", font = "Helvetica 12 bold", command=self.minimizar)
        self.button1.grid(row=2, column=0, padx=5, pady=5)
        self.button2.grid(row=2, column=1, padx=5, pady=5)
        centrarVentana(self.top)
        
    def reiniciar(self):
        os.system("sudo reboot ")
        self.top.destroy()
        self.parent.destroy()
    
    def minimizar(self):
        self.top.destroy()
        self.parent.iconify()
        time.sleep(1)
        self.parent.deiconify()




class MyApp:
    def __init__(self, parent):
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        d = MyDialog(raiz)
        self.parent.wait_window(d.top)

def ProcesarDatos():    
    while True:
        resultado = instanciarSensor()
        if(resultado.is_valid()):
            temperatura = leerTemperatura(resultado)
            valorTemperatura.set("Temperatura: %d C" % temperatura)
            
            humedad = leerHumedad(resultado)            
            valorHumedad.set("Humedad: %d %%" % humedad)            
            if temperatura>31:
                alarmaSonora.activarAlarma()
                alarmaSilenciosa.blink(3,1)
            elif humedad>70:
                alarmaSonora.activarAlarma()
                alarmaSilenciosa.blink(3,1)
            else:
                alarmaSonora.desactivarAlarma()
            time.sleep(1)


if __name__ == "__main__":
    alarmaSonora = puertosGPIO(pin=18,modo="OUT", default=0)
    alarmaSilenciosa = puertosGPIO(pin=21,modo="OUT")
    
    raiz = Tk()#inicializo la raiz
    app = MyApp(raiz)    
    propiedades = properties()

    raiz.title(propiedades.tituloVentana)
    raiz.resizable(propiedades.usuarioModificaAnchoVentana,propiedades.usuarioModificaAltoVentana) 
    raiz.geometry(propiedades.anchoVentana + "x" + propiedades.altoVentana)
    raiz.config(background=propiedades.colorFondo)
    if propiedades.activarFullScreen == True:
        raiz.attributes('-fullscreen', True) #maximizar ventana
    centrarVentana(raiz)
    utilidades = util(raiz)
        

    valorTemperatura = StringVar()
    valorTemperatura.set("35")
    Label(raiz, textvariable=valorTemperatura, font = "Helvetica 12").pack()

    valorHumedad = StringVar()
    valorHumedad.set("35")
    Label(raiz, textvariable=valorHumedad, font = "Helvetica 12").pack()
    
    valorClock = StringVar()
    valorClock.set("35")
    Label(raiz, textvariable=valorClock, font = "Helvetica 12").pack()




    
        
    if os.path.exists(propiedades.imagenFondo):    
        imagenFondo = PhotoImage(file=propiedades.imagenFondo) #https://convertio.co/es/jpg-ppm/        
    else:
        ReiniciarSistema(raiz)
    
        
    Thread(target=ProcesarDatos).start()
    
    #lanzo la raiz
    raiz.mainloop()
    
    
