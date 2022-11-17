import tkinter as tk

class Map :

    def __init__(self, window, width, height) :
        self.width = width  # largeur de la map
        self.height = height  # hauteur de la map
        self.canvas = tk.Canvas(window, width=width, height=height, bg = "grey")  #  zone graphique

    def get_width(self) :
        """
        Retourne la largeur
        """
        return self.width

    def get_height(self) :
        """
        Retourne la hauteur
        """
        return self.height

    def get_canvas(self) :
        """
        Retourne la zone graphique
        """
        return self.canvas
