import random
import math

DIRECTION = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
DIRECTIONS = (((1,-1),(0,-1),(-1,-1)),((1,1),(0,1),(-1,1)),((1,1),(1,0),(1,-1)),((-1,1),(-1,0),(-1,-1)),((0,1),(1,1),(1,0)),((0,1),(-1,1),(-1,0)),((-1,0),(-1,-1),(0,-1)),((0,-1),(1,-1),(1,0)))
class Nest :
    def __init__(self, id_nest, nb_ants, position, map) :
        """
        Un nid composé de nb_ants fourmi est placé en position
        """
        self.id_nest = id_nest
        self.nb_ants = nb_ants
        self.position = position
        self.canv = map.get_canvas()
        self.map = map
        self.resource_pheromone = [] # Contient tous les pheromones de ressources deposés (quand resource trouvé)
        # Pour pouvoir deplacer le nid si on veux ajouter l'option
        #self.id_nest = None #On init l'id dans la fonction affiche_nest

    def affiche_nest(self) :
        """
        Crée le nid sur le canvas
        """
        pos = self.position
        self.canv.create_oval(pos[0]-10,pos[1]-10,pos[0]+10,pos[1]+10,fill="black", tag = "nest")

    def add_resource_pheromone(self,pheromone) :
        """
        Ajoute un pheromone de ressource à la liste des pheromone
        """
        self.resource_pheromone += [pheromone]

    def drop_pheromone(self,idres) :
        """
        Supprime tous les pheromones qui menent vers la ressource 'idres' donné en parametre
        """
        l_pheromone = self.canv.find_withtag(str(idres))
        for f in l_pheromone :
            self.canv.delete(f)
        self.resource_pheromone = []

    def get_pos_nest(self):
        return self.position


class Ant(Nest) :
    def __init__(self,nest,coord):
        """
        Une fourmi
        """
        self.nest = nest
        self.coord = coord # coordonnees de la fourmi
        self.id_ant = None # id de la fourmi
        self.research_pheromone = 1000 # Decremente a chaque deplacement (energy)
        self.state = 'follow' # Etat de la fourmi (follow ou return) return = retour au nid / follow = deplacement
        self.has_res = False # True si la fourmi a une ressource sur elle False sinon
        self.tag_res = [] # Contient l'id de toute les ressource rencontré par la fourmi
        self.actually_res = 0 # index de la derniere ressource rencontré
        self.direction = DIRECTIONS[random.randint(0,7)] # Direction de la fourmi (N,S,E,O,NE,NO,SE,SO)

    def affiche_ant(self) :
        """
        Crée une fourmi sur le canvas
        """
        self.id_ant = self.nest.canv.create_rectangle(self.coord[0],self.coord[1],self.coord[0]+3,self.coord[1]+2,fill="black", tag ='ant')

    def get_pos_ant(self) :
        """
        Retourne les coordonnées de la fourmis
        """
        return self.coord

    def get_state(self) :
        """
        Retourne l'etat de la fourmi ('follow' ou 'return')
        """
        return self.state

    def set_last_resource(self) :
        """
        Met la variable has_res a la valeur 'last' pour indiquer que la ressource est maintennat vide
        """
        self.has_res = 'last'

    def move_is_ok(self,coord) :
        """
        Retourne True si les coordonnées sont dans le canvas False sinon
        """
        # Ps : peut etre ameliorer en recuperant les valeur de la class map directement ??
        if coord == None :
            return False
        if coord[0] < 1 or coord[0]>self.nest.map.get_width()-1:
            return False
        if coord[1] < 1 or coord[1]>self.nest.map.get_height()-1:
            return False
        return True

    def random_move(self) :
        """
        Retourne un vecteur aléatoire dans la direction de la fourmis si possible sinon
        change la direction de la fourmis
        """
        offsets = self.direction
        v = [-1,-1]
        history = []
        while self.move_is_ok(v) == False :
            mvt = offsets[random.randint(0,2)]
            v = (self.coord[0]+mvt[0],self.coord[1]+mvt[1])
            if mvt in history : # On teste si case deja testé
                pass
            else :
                history += [mvt]
            if len(history) >= 3 : #Si les 3 case de la direction deja teste on change de direction
                self.direction = DIRECTIONS[random.randint(0,7)]
                offsets = self.direction
            if len(history) == 8 : # !!! Peut etre enlevé faut tester !!!
                return 0
            # *On regarde maintennat si il n'y a pas d'obvstacle sur la case
            test = self.nest.canv.find_overlapping(self.coord[0]+mvt[0],self.coord[1]+mvt[1],self.coord[0]+mvt[0],self.coord[1]+mvt[1])
            for x in test :
                if 'barrier' in  self.nest.canv.gettags(x) :
                    v = [-1,-1]
        self.research_pheromone  -= 1 # on reduis l'energie
        return v

    def nearest_position(self) :
        """
        Renvoie la postion la plus proche du nid et directement accessible par la fourmis
        """
        pnest = self.nest.get_pos_nest()
        offsets = DIRECTION
        nearest = 10000
        nearestoffset = 0
        for off in offsets :
            test = self.nest.canv.find_overlapping(off[0]+self.coord[0],off[1]+self.coord[1],off[0]+self.coord[0],off[1]+self.coord[1])
            l_tag = []
            for id in test :
                l_tag  += (self.nest.canv).gettags(id)
            if 'barrier' in l_tag :
                pass
            else :
                dist = math.sqrt((pnest[0]-(off[0]+self.coord[0]))**2+(pnest[1]-(off[1]+self.coord[1]))**2)
                if dist < nearest :
                    nearest = dist
                    nearestoffset = off
        return nearestoffset


    def return_to_nest(self) :
        """
        Déplace la fourmis dans la direction du nid
        """
        test = self.nest.canv.find_overlapping(self.coord[0],self.coord[1],self.coord[0],self.coord[1])
        l_tag = []
        for id in test :
            l_tag  += (self.nest.canv).gettags(id)
        if 'nest' in l_tag  :
            # arriver au nid / recharge de pheromone
            self.research_pheromone = 1000
            self.nest.canv.itemconfigure(self.id_ant, fill='black') # froumi deviens noir
            self.state = 'follow' # etat 'follow'
            self.has_res = False # Depose la ressource
            self.direction = DIRECTIONS[random.randint(0,7)] # nouvelle direction aleatoire
        else :
            if self.has_res == 'last' : # cas ressource vide
                nearestoffset = self.nearest_position()
                self.nest.canv.move(self.id_ant,nearestoffset[0],nearestoffset[1])
                self.coord = [self.coord[0]+nearestoffset[0],self.coord[1]+nearestoffset[1]]
            elif self.has_res : # cas ou la fourmi a une resssource sur elle (depose pheromone de ressource)
                test = self.nest.canv.find_overlapping(self.coord[0],self.coord[1],self.coord[0],self.coord[1])
                test_phero = False
                for id in test :
                    if 'pheromone' in self.nest.canv.gettags(id) :
                        test_phero = True
                if test_phero :
                    nearestoffset = self.nearest_position()
                    self.nest.canv.move(self.id_ant,nearestoffset[0],nearestoffset[1])
                    self.coord = [self.coord[0]+nearestoffset[0],self.coord[1]+nearestoffset[1]]
                else :
                    f = self.nest.canv.create_rectangle(self.coord[0]-2,self.coord[1]-2,self.coord[0]+2,self.coord[1]+2,fill='',outline='',tag=('pheromone','pheromone'+str(self.nest.id_nest),str(self.tag_res[self.actually_res])))
                    self.nest.add_resource_pheromone(f)
                    id = self.nest.canv.create_rectangle(self.coord[0]-2,self.coord[1]-2,self.coord[0]+2,self.coord[1]+2,fill='red',outline='')
                    self.nest.canv.tag_lower(id)
                    nearestoffset = self.nearest_position()
                    self.nest.canv.move(self.id_ant,nearestoffset[0],nearestoffset[1])
                    self.coord = [self.coord[0]+nearestoffset[0],self.coord[1]+nearestoffset[1]]
            else : # cas retour au nid normal (plus de pheromone)
                nearestoffset = self.nearest_position()
                self.nest.canv.move(self.id_ant,nearestoffset[0],nearestoffset[1])
                self.coord = [self.coord[0]+nearestoffset[0],self.coord[1]+nearestoffset[1]]


    def find_pheromone(self) :
        """
        Renvoie la position d'une pheromone si il y en a une à proximité sinon appelle la fonction random_move
        """
        pnest = self.nest.get_pos_nest()
        offsets = DIRECTION
        distmax = 0
        f = None
        # Recherche si il y a des pheromone a cote
        for off in offsets :
            if self.move_is_ok([self.coord[0]+off[0],self.coord[1]+off[1]]) :
                test = self.nest.canv.find_overlapping(self.coord[0]+off[0],self.coord[1]+off[1],self.coord[0]+off[0],self.coord[1]+off[1])
                l_tag = []
                for id in test :
                    l_tag  += self.nest.canv.gettags(id)
                if 'pheromone'+str(self.nest.id_nest) in l_tag :
                    dist = math.sqrt((pnest[0]-(off[0]+self.coord[0]))**2+(pnest[1]-(off[1]+self.coord[1]))**2)
                    if dist > distmax :
                        distmax = dist
                        f = [self.coord[0]+off[0],self.coord[1]+off[1]]
        if f == None :
            return self.random_move()
        else :
            return f


    def find_resource(self) :
        """
        Renvoie la position d'une ressource si elle se trouve à proximité et retourne la fourmis
        au nid si elle a trouvé une ressource.
        """
        offsets = DIRECTION
        # On regarde si elle se trouve sur une ressource
        test = self.nest.canv.find_overlapping(self.coord[0],self.coord[1],self.coord[0],self.coord[1])
        l_tag = []
        for id in test :
            l_tag  += self.nest.canv.gettags(id)
        if 'resource' in l_tag :
            self.nest.canv.itemconfigure(self.id_ant, fill='red')
            self.state = 'return'
            self.has_res = True
            for tag in l_tag :
                if tag != 'resource' and tag != 'ant' and tag!='pheromone' and tag != 'nest':
                    if tag not in self.tag_res :
                        self.tag_res += [tag]
                        self.actually_res = len(self.tag_res)-1
                    else :
                        self.actually_res = self.tag_res.index(tag)
            self.state = 'return'
            self.return_to_nest()
            return 0
        # On regarde autour de la fourmi si il y a une ressource
        for off in offsets :
            le_mvt = [self.coord[0]+off[0],self.coord[1]+off[1]]
            if self.move_is_ok(le_mvt) :
                test = self.nest.canv.find_overlapping(self.coord[0]+off[0],self.coord[1]+off[1],self.coord[0]+off[0],self.coord[1]+off[1])
                l_tag = []
                for id in test :
                    l_tag  += self.nest.canv.gettags(id)

                if 'resource' in l_tag :
                    return [self.coord[0]+off[0],self.coord[1]+off[1]]


    def move_ant(self) :
        """
        Déplace la fourmi sur le Canvas
        """
        if self.research_pheromone < 1 :
            # si plus de pheromone
            self.nest.canv.itemconfigure(self.id_ant, fill='')
            self.state = 'return'
            return 0
        food_pos = self.find_resource() # on recherche des ressource a proximité
        if food_pos == 0 : # cas ou elle est sur la resource donc on passe
            pass
        elif self.move_is_ok(food_pos) :
            self.nest.canv.move(self.id_ant,food_pos[0]-self.coord[0],food_pos[1]-self.coord[1])
            self.coord = food_pos
        else :
            pos = self.find_pheromone() # on recherche des pheromone a proximité
            if pos == 0 :
                return 0
            self.nest.canv.move(self.id_ant,pos[0]-self.coord[0],pos[1]-self.coord[1])
            self.coord = pos
        return 0
