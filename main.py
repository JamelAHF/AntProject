from tkinter import *
from tkinter import messagebox
import nest
import resource
import time
import random
import map
import simulation
import barrier

# variables globales

# fenetre du nb de fourmis d'un nid et de la quantite de ressources
win_nest, win_res = None, None
# nb max de fourmis dans un nid, nb max de quantite d'une ressource
max_ants, max_qtres = 200, 500

# nb actuel de nids et de ressources
c_nest, c_res = 0, 0

# nb max de nids et de ressources
max_nest, max_res = 4, 4

# statut en cours, 0 = barriere, 1 = nid, 2 = ressource
current = 0

class Interface(Tk):

    def __init__(self):

        Tk.__init__(self)

        #  taille de la fenetre
        width = 1200
        height = 650
        self.geometry(str(width)+"x"+str(height))

        #  titre de la fenetre
        self.title("Ants Viewer")

        self.themap = map.Map(self, width-300, height-70)
        # creer simulation
        self.simu = simulation.Simulation(self.themap.get_canvas(), 10, 0)

        #  je cree la zone graphique
        self.graphiczone()

        #  message affiche dans la barre du bas
        self.mess_statusbar = StringVar()

        #  barre de menu
        self.toolbar()

        #   variables contenant le nb de fourmis du nid, quantite de la ressource
        self.ants, self.res = StringVar(), StringVar()
        self.ants.set(50)
        self.res.set(50)

        #   variables contenant le message indiquant si le nb de fourmis/la quantite est correct.
        self.mess_nest, self.mess_res = StringVar(), StringVar()

        # à supprimer


        #  barre contenant les boutons
        self.buttons_bar()

        #  barre d'etat
        self.statusbar()

        self.mainloop()

    #  ZONE GRAPHIQUE ET FONCTIONS


    def add_sth(self, x, y):
        """
        Ajoute une barrière, un nid ou une ressource selon la valeur de current
        """
        global current, c_nest, c_res
        stat = self.simu.status  # statut de la simulation

        # si on cree un obstacle
        if current == 0:
            if stat != -1:  # si la simulation n'est pas terminé
                bar = barrier.Barrier(self.themap.get_canvas(), [x,y])
                bar.create_barrier()
            else:
                messagebox.showinfo("Simulation is finished", "You can't add a barrier after the end of the simulation.")

        # si on cree un nid
        elif current == 1:
            if (c_nest < max_nest):  # verif si dépasse pas le nb max de nids autorisé
                # on recup le nb de fourmis
                nb_ants = int(self.ants.get())
                # on cree le nid et l'ajoute
                nid = nest.Nest(c_nest, nb_ants, (x,y), self.themap)
                self.simu.add_nest(nid)
                # on l'affiche
                nid.affiche_nest()

                # on ajoute les fourmis
                for i in range(nb_ants) :
                    # je place la fourmi aléatoirement autour du nid
                    m, n = random.randint(x-10,x+10), random.randint(y-10,y+10)
                    ant = nest.Ant(nid,(m,n))
                    ant.affiche_ant()
                    self.simu.add_ant(ant)

                #  on incremente le nb de nids actuel
                c_nest += 1
            else:
                messagebox.showinfo("Number of nests excedeed", "The number of nests is excedeed (max. {})".format(max_nest))

        # si on cree une ressource
        elif current == 2:

            if (c_res < max_res): # verif si le nb max de ressources est pas depasse
                nb_res = int(self.res.get())  # recup de la quantite de la ressource
                ress = resource.Resource("res"+str(c_res), self.themap.get_canvas(), nb_res, (x,y))
                self.simu.add_res(ress)
                ress.affiche_resource()

                c_res += 1  #  on incremente le nb de ressources actuel
            else:
                messagebox.showinfo("Number of resources excedeed", "The number of resources is excedeed (max. {})".format(max_res))

        # on remet par defaut
        current = 0

    def graphiczone(self):
        """
        Biding de la map
        """

        (self.themap.get_canvas()).bind('<Button-1>', lambda event: self.add_sth(event.x, event.y))
        (self.themap.get_canvas()).pack()


    #  GESTION DES NIDS

    def bydef_nest(self):
        """
        Met la valeur par défaut pour le nb de fourmis d'un nid.
        """
        global win_nest
        self.ants.set(50)
        win_nest.destroy()

    def verif_nest(self):
        """
        Vérifie si le nombre de fourmis est bien correct (cela doit être un nombre inférieur à la limite).
        """
        global win_nest, current

        # je recupere la valeur entrée dans le champ
        nb_ants = self.ants.get()

        if nb_ants.isdigit():  # si on rentre un nombre
            nb_ants = int(nb_ants)
            # on verifie si le nombre ne dépasse pas la limite
            if (nb_ants < 1 or nb_ants > max_ants):
                self.mess_nest.set("The number must be between 1 and {}.".format(max_ants))
            else:
                win_nest.destroy()  # si c'est correct, on ferme la fenetre
                current = 1  # on passe le statut en mode "nid"
                self.mess_statusbar.set("You add a nest with {} ants.".format(nb_ants))  #  informations dans la barre d'état

        # autres cas (incorrect)
        else:
            self.mess_nest.set("You must insert only numbers.")


    def open_nest(self):
        """
        Ouvre la fenêtre où l'utilisateur pourra choisir le nombre de fourmis du nid
        """
        if self.simu.status != 0:
            messagebox.showinfo("Simulation has started", "You can't add a nest after the launching of the simulation.")
        else:
            global win_nest
            win_nest = Toplevel(self)
            win_nest.protocol('WM_DELETE_WINDOW',self.bydef_nest)  # met la valeur par defaut qd on ferme la fenetre
            win_nest.title("Number of ants")
            win_nest.geometry("300x150")

            Label(win_nest, text ="Choose the number of ants (max. {})".format(max_ants)).pack()
            Entry(win_nest, textvariable = self.ants).pack()
            Button(win_nest, text = "Submit", command= self.verif_nest).pack()
            Label(win_nest, textvariable = self.mess_nest).pack()  # indication en cas d'erreur

    # GESTION DES RESSOURCES

    def bydef_res(self):
        """
        Met la valeur par défaut pour la quantité d'une ressource.
        """
        global win_res
        self.res.set(50)
        win_res.destroy()

    def verif_res(self):
        """
        Vérifie si le nombre de fourmis est bien correct (cela doit être un nombre inférieur à la limite).
        """
        global win_res, current

        # je recupere la valeur entrée dans le champ
        nb_res = self.res.get()

        if nb_res.isdigit():  # si on rentre un nombre
            nb_res = int(nb_res)
            # on verifie si le nombre ne dépasse pas la limite
            if (nb_res < 1 or nb_res > max_qtres):
                self.mess_res.set("The number must be between 1 and {}.".format(max_qtres))
            else:
                win_res.destroy()  # on ferme la fenêtre
                current = 2  # on passe le statut en mode "ressource"
                self.mess_statusbar.set("You add a resource of {}.".format(nb_res))  # informations dans la barre d'état

        # autres cas (incorrect)
        else:
            self.mess_res.set("You must insert only numbers.")

        return True

    def open_res(self):
        """
        Ouvre la fenêtre où l'utilisateur pourra choisir la quantité de la ressource.
        """
        if self.simu.status != 0:
            messagebox.showinfo("Simulation has started", "You can't add a resource after the launching of the simulation.")
        else:
            global win_res
            win_res = Toplevel(self)
            win_res.protocol('WM_DELETE_WINDOW',self.bydef_res)  # met la valeur par defaut qd on ferme la fenetre
            win_res.title("Quantity of resource")
            win_res.geometry("300x150")

            Label(win_res, text ="Choose the quantity of resource (max. {})".format(max_qtres)).pack()
            Entry(win_res, textvariable = self.res).pack()
            Button(win_res, text = "Submit", command= self.verif_res).pack()
            Label(win_res, textvariable = self.mess_res).pack()

    def reset_all(self):
        # si la simulation est terminé ou pas lancé on peut reset
        if self.simu.status == -1 or self.simu.status == 0:
            global c_nest, c_res
            c_nest, c_res = 0, 0
            self.simu.reset_simulation()
        else:
            #  message indiquant que la simulation doit être terminée pour remettre à zéro
            messagebox.showinfo("Simulation not finished", "To reset the simulation, you have to finish the simulation.")


    # menu du bas
    def buttons_bar(self):
        mb = Frame(self)
        mb.pack()
        Button(mb, text="Add a nest", fg="white", bg="#000000", command=self.open_nest).pack(side = LEFT)
        Button(mb, text="Add a resource", fg="white", bg="#C02A0A",command=self.open_res).pack(side = LEFT)

        Button(mb, text = "Start", command=self.simu.start_simulation).pack(side = LEFT)
        Button(mb, text = "Stop", command= self.simu.stop_simulation).pack(side = LEFT)
        Button(mb, text = "Finish", command= self.simu.finish_simulation).pack(side = LEFT)
        Button(mb, text = "Reset", fg="black", bg="#FFFFFF", command = self.reset_all).pack(side = LEFT)

        Button(mb, text = "+ vitesse", fg="white", bg="#0845C1", command= self.simu.speed_up).pack(side = LEFT)
        Button(mb, text = "- vitesse", fg="white", bg="#0845C1", command= self.simu.speed_down).pack(side = LEFT)

    #  BARRE D'ETAT
    def statusbar(self):
        #  contient ...
        statusbar = Label(self, textvariable = self.mess_statusbar, bd=1, relief=SUNKEN, anchor=W)
        #  je place la barre d'etat en bas
        statusbar.pack(side=BOTTOM, fill=X)


    #  BARRE DE MENU
    def toolbar(self):

        toolbar = Menu(self)

        #  Menu file
        file = Menu(toolbar, tearoff=0)
        toolbar.add_cascade(label="File", menu=file)
        file.add_command(label="New", command=self.reset_all)
        file.add_separator()
        file.add_command(label="Quit", command=self.quit)


        #  Menu help
        help = Menu(toolbar, tearoff=0)
        toolbar.add_cascade(label="Help", menu=help)
        help.add_command(label="Functioning", command=self.mhelp)
        help.add_command(label="About", command=self.about)

        self.config(menu = toolbar)


    #  #  #   FONCTIONS DE LA BARRE DE MENU #  #  #

    def quit(self):
        """
        Quitter l'application.
        """
        if messagebox.askokcancel("Quit","Do you really want to quit ?"):
            self.destroy()

    def about(self):
        """
        Affichage du menu "A propos".
        """
        messagebox.showinfo("About", "Project UML\n- By ALI-HADEF, FERNANDES DE FARIA, SAHLI")

    def mhelp(self):
        """
        Affichage du fonctionnement de l'application.
        """
        messagebox.showinfo("Functioning", "1. Add nests and resources\n\n2. Start the simulation")

if __name__=="__main__":
    root = Interface()
