class Barrier :
    def __init__(self,canv,position) :
        self.canv = canv
        self.position = position  # position de la barrière

    def create_barrier(self) :
        """
        Crée une barrière
        """
        self.canv.create_rectangle(self.position[0],self.position[1],self.position[0]+5,self.position[1]+5,fill="black", tag ='barrier')
