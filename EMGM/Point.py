# -*- coding: utf-8 -*-

class Point:
    """
    Representacion de un punto
    """

    def __init__(self, coordinates):
        self.coordinates = coordinates #coordenadas x,y
        self.dimension = len(coordinates) #siempre es 2

    #printable representation    
    def __repr__(self):
        return 'Coordenadas: ' + str(self.coordinates)
