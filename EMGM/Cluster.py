# -*- coding: utf-8 -*-
"""
Created on Sat Apr 01 19:43:20 2017

@author: mario
"""

import numpy as np


class Cluster:
    """
    Representar un cluster: (set de puntos en forma elipsoidal)
    Parametros obligatorios: media, SD, PROB de cada cluster
    """

    def __init__(self, points, total_points):
        #inicializacion
        if len(points) == 0:
            raise Exception("Error! Un cluster no puede tener 0 puntos\n (O mas bien no puede no tener puntos)")
        else:
            #PUNTOS INICIALES DEL CLUSTER
            self.points = points
            self.dimension = points[0].dimension
            print "***Coordenadas iniciales***"
            print ">: ",points[0]

        # Revisar que todos los puntos esten en 2D en este caso
        for p in points:
            if p.dimension != self.dimension:
                raise Exception(
                    "El punto " + str(p) + " tiene dimension "+str(len(p))+"D diferente de resto que tiene dimension: "+str(self.dimension))
        
        # Calcular Media, SD, Prob de cada uno.. Ver convergencia
        #NUMPY!
        points_coordinates = [p.coordinates for p in self.points]
        self.mean = np.mean(points_coordinates, axis=0)
        self.std = np.array([1.0, 1.0])
        self.cluster_probability = len(self.points) / float(total_points)
        self.converge = False

    def update_cluster(self, points, total_points):
        """
        ver si converge cada  cluster
        (Maximization step)
        """
        old_mean = self.mean
        self.points = points
        points_coordinates = [p.coordinates for p in self.points]
        self.mean = np.mean(points_coordinates, axis=0)
        self.std = np.std(points_coordinates, axis=0, ddof=1)
        self.cluster_probability = len(points) / float(total_points)
        self.converge = np.array_equal(old_mean, self.mean)

    def __repr__(self):
        cluster = 'Media: ' + str(self.mean) + '\nDimension: ' + str(
            self.dimension)
        for p in self.points:
            cluster += '\n' + str(p)

        return cluster + '\n\n'
