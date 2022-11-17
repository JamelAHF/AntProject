import tkinter as tk
from tkinter import messagebox
import nest

class Simulation :
    def __init__(self, map, speed, status):
        self.map = map
        self.speed = speed  # vitesse
        self.status = 0  #  état de la simulation, -1 -> arrêté, 0 -> pas lancé, 1-> lancé, 2-> stoppé
        self.l_res = []  #  liste des ressources
        self.l_nest = []  #  liste des nids
        self.l_ants = []  # liste des fourmis
        self.res_sup = []

    # ASSESSEURS
    def add_nest(self, nest):
        """
        Ajoute un nid à la liste des nids
        """
        self.l_nest += [nest]

    def add_ant(self, ant):
        """
        Ajoute une fourmi à la liste de fourmis
        """
        self.l_ants += [ant]

    def add_res(self, res):
        """
        Ajoute une ressource à la liste des ressources
        """
        self.l_res += [res]


    def start_simulation(self):
        """
        Démarre la Simulation
        """
        if self.status == 0 or self.status == 2:
            self.status = 1
            self.simulation()

    def stop_simulation(self):
        """
        Arrête la simulation
        """
        self.status = 2

    def finish_simulation(self):
        """
        Termine la simulation, ce qui permet de la remettre à zero
        """
        self.status = -1

    def reset_simulation(self):
        """
        Remet la simulation à zéro si cette dernière est terminée
        """
        self.map.delete("all")
        self.status = 0
        self.l_res = []
        self.l_nest = []
        self.l_ants = []

    # GESTION DE LA VITESSE

    def speed_up(self):
        """
        Augmente la vitesse de la simulation
        """
        if self.speed > 10 :
            self.speed -= 5

    def speed_down(self):
        """
        Baisse la vitesse de la simulation
        """
        if self.speed < 30:
            self.speed += 5

    def simulation(self) :
        """
        Gestion automatique de la simulation
        """
        for res in self.res_sup :
            for n in self.l_nest :
                n.drop_pheromone(res)
        for a in self.l_ants :
            if a.get_state() == 'follow' :
                a.move_ant()
                for i in range(len(self.l_res)) :
                    ress = self.l_res[i]
                    if ress != False :
                        pos_ant = a.get_pos_ant()
                        test = (self.map).find_overlapping(pos_ant[0],pos_ant[1],pos_ant[0],pos_ant[1])
                        l_tag = []
                        for id in test :
                            l_tag  += (self.map).gettags(id)
                        if 'resource' in l_tag  :
                            if ress.get_ide_resource() in l_tag :
                                test = ress.reduce_resource()
                                if test:
                                    a.set_last_resource()
                                    ress.drop_resource()
                                    self.l_res[i]=False
                                    self.res_sup += [ress.get_ide_resource()]
            elif a.get_state() == 'return' :
                a.return_to_nest()
        if self.status == 1 :
            self.map.after(self.speed, self.simulation)
