""" Importamos el modelo del archivo en que lo definimos. """
from robotsModel import Almacen

""" matplotlib lo usaremos crear una animación de cada uno de los pasos
    del modelo. """
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128

""" Importamos los siguientes paquetes para el mejor manejo de valores
    numéricos."""
import numpy as np
import pandas as pd
import random

""" Definimos otros paquetes que vamos a usar para medir el tiempo de
    ejecución de nuestro algoritmo. """
import time
import datetime

""" Tamaño de la Almacen """
M = 10
N = 10

""" Numero de Robots """
R = 5

""" Numero de Cajas """
K = 10

""" Tiempo máximo de ejecución"""
MAX_GENERATIONS  = .1

""" Registramos el tiempo de inicio y guardamos e tiempo que tardo en ordenar las cajas. """
iniciarTiempo = time.time()
modelo = Almacen(M, N, K)

while((time.time() - iniciarTiempo) < MAX_GENERATIONS):
    modelo.step()
    if(modelo.contCajas != K):
        """ Guardamos el tiempo que le tomó correr al modelo. """
        tiempoTranscurrido = time.time() - iniciarTiempo

""" Obtenemos la información que almacenó el colector, este nos entregará un
    DataFrame de pandas que contiene toda la información. """
infoModel = modelo.colectorDatos.get_model_vars_dataframe()

""" Graficamos la información usando `matplotlib` """
fig, axs = plt.subplots(figsize=(7,7))
axs.set_xticks([])
axs.set_yticks([])
patch = plt.imshow(infoModel.iloc[0][0], cmap='binary')

def animate(i):
    patch.set_data(infoModel.iloc[i][0])

anim = animation.FuncAnimation(fig, animate, frames=len(infoModel))
plt.show()

""" Visualizamos los datos de salida """
print('Almacen de ', M, 'x', N)
print('Numero de Cajas: ', K)
print('Numero de Robots: ', R)
print('')
print('Número de movimientos realizados por todos los agentes:', modelo.numSteps)
print('Tiempo necesario para apilar todas las cajas:', tiempoTranscurrido)