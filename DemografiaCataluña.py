#Deben descargar primero el archivo: "DemografiaCat2017.sqlite" en: 
https://github.com/DataAnalysisCases/Juan-Pablo-Delzo/blob/master/DemografiaCat2017.sqlite

############################IMPORTANDO LIBRERIAS##################
#Entornos del tkinter:
import tkinter as tk
from tkinter import ttk
from tkinter  import font
from PIL import ImageTk,Image
from io import BytesIO
from urllib.request import urlopen
import os
#Para crear los gráficos:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#SQLite:
import sqlite3

################EXTRAYENDO DATOS##################################
connection = sqlite3.connect('DemografiaCat2017.sqlite')
cursor = connection.cursor()
datos= cursor.execute("SELECT name FROM sqlite_master WHERE type= 'table'").fetchall()
municipios =[]
for dato in datos:
    municipios.append(dato[0])
#Variables globales:
color='black'
wb=100
hb=30
#Colores del gráfico:
col=['red','blue']

#######################FUNCIONES:###############################

#Buscador de municipios:
def buscador():
    listbox.delete(0,tk.END)
    termino= e.get()
    lista=[]
    for municipio in municipios:
        if termino[1:].lower() in municipio:
            lista.append(municipio)
    if len(lista) == 0:
        label2.config(text= '¡NO COINCIDE CON LA BASE DE DATOS!')
    else:
        label2.config(text= '')
        for item in lista:
            listbox.insert(tk.END,item)
    e.delete(0,tk.END)
#Coge el municipio clickado:
def CurSelect(evt):
    labelesp.config(text='¡Tarda unos segundos!')
    global municipio
    municipio= listbox.get(tk.ANCHOR)
#Graficando:
def graficar():
    df = pd.read_sql_query("SELECT * FROM `{0}`".format(municipio), connection)
    data= pd.DataFrame({'hombres':df.hombres,'mujeres':df.mujeres})
    #Texto del total de la población:
    total= df.total[len(df.total)-1]
    total= str(total)
    if len(total) >6:
        total= total[:-6]+"'"+total[-6:-3]+'.'+total[-3:]
    elif len(total) > 3:
        total= total[:-3]+'.'+total[-3:]
    plt.style.use('dark_background')
    fig=plt.figure(figsize=(7,6))
    #Barchar horizontal:
    ax1=fig.add_subplot(3,1,(1,2)) 
    data[:-1].plot.barh(color= col,stacked= True,ax= ax1)
    ax1.set_yticks(range(len(df.total[:-1])))
    ax1.set_yticklabels(df.edad[:-1])
    ax1.set_xlabel('Habitantes')
    ax1.set_ylabel('Edades')
    for i,v in enumerate(df.total[:-1]):
        ax1.text(v,i,str(v),color= 'white',fontweight='bold')
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.legend(loc='best')
    #Piechart:
    ax2=fig.add_subplot(3,2,5)
    piedato = [data.hombres[11],data.mujeres[11]]
    wedges, texts, autotexts= ax2.pie(piedato, colors= col, autopct='%1.0f%%',shadow= True,startangle=90)
    #Texto del total de la poblacion:
    ax3=fig.add_subplot(3,2,6)
    ax3.text(0.0,0.5,total + ' hab.',fontsize=19,fontweight='bold')
    ax3.xaxis.set_major_locator(plt.NullLocator())
    ax3.yaxis.set_major_locator(plt.NullLocator())
    ax3.spines['bottom'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    #Ajustes:
    plt.setp(autotexts, size=10, weight="bold")
    fig.suptitle(municipio, y = 1,fontsize=23)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    file= municipio + '.png'
    plt.savefig(file)
    plt.close(fig)
    img1 = ImageTk.PhotoImage(Image.open(file))
    labelimage.config(image=img1)
    labelimage.image = img1
    labelesp.config(text='')

############ROOT:#############################
root= tk.Tk()
ancho=root.winfo_screenwidth()
altura=root.winfo_screenheight()
strink= '{}x{}'.format(ancho,altura)
root.geometry(strink)
root.title('Demografia de los municipios de Catalunya 2017')

####################CANVAS:##############################
w=tk.Canvas(root,bg= color,width= ancho,height= altura)
w.place(x=0,y=0)

############INPUT:###############
#Etiqueta de municipio:
label=tk.Label(w,text= 'Municipio:',font=('Arial',14),bg= color,justify= 'left' , fg = 'white')
label.place(x=ancho//20,y=altura//20)
#Etiqueta de advertencia cuando el input no coincide con la base de datos:
label2=tk.Label(w,text= '',font=('STENCIL',13),bg=color,justify= 'left',fg= 'white')
label2.place(x=ancho//20,y=3*altura//20)
#Advertencia para esperar:
labelesp = tk.Label(w,text='',font= ('ALGERIAN',15),bg= color, fg= 'white')
labelesp.place(x=ancho//20,y=11*altura//20)
#Input:
e=tk.Entry(w)
e.place(x=ancho//20,y=2*altura//20)

#python_url= "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
#Etiqueta de imagen inicial(Matplotlib):
mpl_url= "http://matplotlib.sourceforge.net/_static/logo2.png"
img_file = urlopen(mpl_url).read()
im = Image.open(BytesIO(img_file))
image = ImageTk.PhotoImage(im)
labelimage= tk.Label(w,image= image,bg= color)
labelimage.place(x= 3*ancho//4,y= altura//2,anchor= 'c',width=ancho//2,height= 4*altura//5)

#############LISTBOX:##########################
listbox = tk.Listbox(w)
listbox.place(x=ancho//20,y=6*altura//20,width=2.5*wb,anchor= 'nw')
scrollbar=tk.Scrollbar(w,command=listbox.yview)
scrollbar.place(in_=listbox,relx=1.0,relheight=1.0,bordermode='outside')
listbox.config(yscrollcommand=scrollbar.set)
listbox.bind('<<ListboxSelect>>',CurSelect)

#############BOTONES:#########################
#Editando el estilo de texto:
style = ttk.Style(root)
Sys14 = font.Font(family='System', size=14, weight='bold')
style.configure("TButton", font=Sys14)

#Boton Salida:
b1=ttk.Button(w,text='Salir',command= root.destroy, style="TButton" )
b1.place(x=4*ancho//10,y=16*altura//20,width=wb,height=hb)
#Boton de Calculo:
b2=ttk.Button(w,text='Consultar',command= graficar, style="TButton")
b2.place(x=4*ancho//10,y=9*altura//20,width=wb,height=hb)
#Buscador de municipios:
b3=ttk.Button(w,text= 'Buscar',command= buscador, style="TButton")
b3.place(x=4*ancho//10,y=2*altura//20,width=wb,height=hb)

####################### Root Loop #######################################################
root.mainloop()
