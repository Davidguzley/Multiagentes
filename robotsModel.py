# Importamos las clases que se requieren para manejar los agentes (Agent) y su entorno (model).
# Cada model puede contener múltiples agentes.
from mesa import Agent, Model

# Debido a que necesitamos que existe un solo agente por celda, elegimos ''MultiGrid''.
from mesa.space import MultiGrid

# Con ''SimultaneousActivation, hacemos que todos los agentes se activen ''al mismo tiempo''.
from mesa.time import SimultaneousActivation

# Haremos uso de ''DataCollector'' para obtener información de cada paso de la simulación.
from mesa.datacollection import DataCollector

# Importamos los siguientes paquetes para el mejor manejo de valores numéricos.
import numpy as np
import pandas as pd
import random

def obtenerAlmacen(model):
    grid = np.zeros( (model.grid.width, model.grid.height) )
    for (content, x, y) in model.grid.coord_iter():
        for contenido in content: 
            if isinstance(contenido, Caja):
                if contenido.state == contenido.esCaja:
                    if contenido.pila ==  5:
                        grid[x][y] = 4
                else:
                    grid[x][y] = 1
            if isinstance(contenido, Robot):
                if contenido.status == 0:
                    grid[x][y] = 6
                else:
                    grid[x][y] = 6
    return grid

class Robot(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.next = None
        self.status = False
        self.x, self.y = pos
    
    def step(self):
        if self.status == False:
            neighbours = self.model.grid.get_neighbors(self.pos, moore = False, include_center = True)
            for neighbor in neighbours:
                if neighbor.pos == self.pos:
                    if (neighbor.state == neighbor.noCaja and 
                        self.status == False):
                        neighborhood = self.model.grid.get_neighborhood(self.pos, moore = False, include_center = True)
                        self.next = self.random.choice(neighborhood)
                    else:
                        if(neighbor.pila == 0 and 
                            self.status == False):
                            neighbor.state = neighbor.noCaja
                            self.status = True
                            self.next = self.pos
                        else:
                            neighborhood = self.model.grid.get_neighborhood(self.pos, moore = False, include_center = True)
                            self.next = self.random.choice(neighborhood)
                    break
        else:
            if self.x != self.model.moveStackX:
                self.x -= 1
            elif self.x == self.model.moveStackX:
                if self.y != self.model.moveStackY:
                    if self.y < 0:
                        self.y = self.model.width - (self.y * -1) % self.model.width
                    self.y -= 1
                elif self.y == self.model.moveStackY:
                     
                    neighbours = self.model.grid.get_neighbors(self.pos, moore = False, include_center = True)
                    for neighbor in neighbours:
                        if isinstance(neighbor, Caja):
                            if neighbor.pos == self.pos:                             
                                if neighbor.state == neighbor.noCaja:
                                    neighbor.state = neighbor.esCaja
                                    self.model.contCajas += 1
                                    neighbor.pila = 1
                                    self.status = False
                                    self.x += 1
                                    
                                else:
                                    if (neighbor.pila == 4):
                                        neighbor.pila += 1
                                        self.status = False
                                        self.model.contCajas += 1
                                        self.model.moveStackY += 1
                                        self.x += 1
                                        
                                        if self.model.moveStackY == self.model.width - 2:
                                            self.model.moveStackX += 1
                                            self.model.moveStackY = 0
                                        
                                    else:
                                        neighbor.pila += 1
                                        self.model.contCajas += 1
                                        self.status = False
                                        self.x += 1
                
                                break
            
            self.next = self.x, self.y
                    
        self.model.grid.move_agent(self, self.next)

class Caja(Agent):
    esCaja = 1
    noCaja = 0
    
    def __init__(self, pos, model, state = noCaja):
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = state
        self.pila = 0

class Almacen(Model):
    def __init__(self, width, height, K):
        self.K = K
        self.moveStackY = 0
        self.moveStackX = 0
        self.width = width
        self.numRobots = 5
        self.grid = MultiGrid(width, height,True)
        self.schedule = SimultaneousActivation(self)
        self.numSteps = 0
        self.contCajas = 0
        
        
        emptys = list(self.grid.empties)
        for cells in range(self.K):
            cajaNum = random.choice(emptys)
            caja = Caja(cajaNum, self)
            caja.state = caja.esCaja
            self.grid.place_agent(caja, cajaNum)
            self.schedule.add(caja)
            emptys.remove(cajaNum)
            
        emptys = list(self.grid.empties)
        for cells in emptys:
            celdaLibre = Caja(cells, self)
            celdaLibre.state = celdaLibre.noCaja
            self.grid.place_agent(celdaLibre, cells)
            self.schedule.add(celdaLibre)
            
        i = 0
        while (i<=4):
            if i == 0:
                x = random.randint(0, height - 1)
                y = random.randint(0, width - 1)
                robot = Robot(i, self, (x,y))
                self.grid.place_agent(robot, (x,y))
                self.schedule.add(robot)
                i = i + 1
            if i == 1:
                x = random.randint(0, height - 1)
                y = random.randint(0, width - 1)
                robot = Robot(i, self, (x,y))
                self.grid.place_agent(robot, (x,y))
                self.schedule.add(robot)
                i = i + 1
            if i == 2:
                x = random.randint(0, height - 1)
                y = random.randint(0, width - 1)
                robot = Robot(i, self, (x,y))
                self.grid.place_agent(robot, (x,y))
                self.schedule.add(robot)
                i = i + 1
            if i == 3:
                x = random.randint(0, height - 1)
                y = random.randint(0, width - 1)
                robot = Robot(i, self, (x,y))
                self.grid.place_agent(robot, (x,y))
                self.schedule.add(robot)
                i = i + 1
            if i == 4:
                x = random.randint(0, height - 1)
                y = random.randint(0, width - 1)
                robot = Robot(i, self, (x,y))
                self.grid.place_agent(robot, (x,y))
                self.schedule.add(robot)
                i = i + 1
            
        self.colectorDatos = DataCollector(model_reporters = {'Grid': obtenerAlmacen})
        
    def step(self):
        self.colectorDatos.collect(self)
        self.schedule.step()
