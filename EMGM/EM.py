# -*- coding: utf-8 -*-
"""
Created on Sat Apr 01 19:43:20 2017

@author: mario
"""

import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from Point import Point
from Cluster import Cluster

#DATASET1 = "./dataSet/DS_3Clusters_999Points.txt"
#DATASET2 = "./dataSet/DS2_3Clusters_999Points.txt"
DATASET3 = "./dataSet/DS_5Clusters_10000Points.txt"
#DATASET4 = "./dataSet/DS_7Clusters_100000Points.txt"

puntos = []
# Constantes
ITERATIONS = 1000
COLORS = ['red', 'blue', 'green', 'yellow', 'gray', 'orange', 'violet', 'brown',
          'cyan', 'magenta']
          



def dataset_to_list_points(dir_dataset):
    """
    Del path file txt leo un set de puntos
    Regreso una lista de puntos (lista de listas)-> [[],[],[],[]]
    """
    points = list()
    with open(dir_dataset, 'rt') as reader:
        for point in reader:
            points.append(Point(np.asarray(map(float, point.split(",")))))
    return points


def get_probability_cluster(point, cluster):
    """
    Calcula la probabilidad de que un punto pertenezca a un cluster
    probabilidad =
    prob * SUM(e ^ (-1/2 * ((x(i) - mean)^2 / std(i)^2 )) / std(i))
    
    #ESPERANZA
    """
    mean = cluster.mean
    std = cluster.std
    prob = 1.0
    for i in range(point.dimension):
        prob *= (math.exp(-0.5 * (
            math.pow((point.coordinates[i] - mean[i]), 2) /
            math.pow(std[i], 2))) / std[i])

    return cluster.cluster_probability * prob #normalizar PI

def get_expectation_cluster(clusters, point):
    """
    Devuelve cluster con mayor probabilidad
    """
    expectation = np.zeros(len(clusters))
    for i, c in enumerate(clusters):
        expectation[i] = get_probability_cluster(point, c)

    return np.argmax(expectation) #devuelve el indice maximo


def print_clusters_status(it_counter, clusters):
    print '\nITERACION %d' % it_counter
    for i, c in enumerate(clusters):
        print '\tCluster %d: Probabilidad = %s; Media = %s; Std = %s; Total Puntos Actuales = %s' % (
            i + 1, str(c.cluster_probability), str(c.mean), str(c.std), str(len(c.points)))


def print_resultados(clusters):
    print '\t\t**************RESULTADO************'
    for i, c in enumerate(clusters):
        print '\tCluster %d' % (i + 1)
#        print c.points
        print '\t\tTotal de Puntos en el Cluster: %d' % len(c.points)
        print '\t\tProbabilidad: %s' % str(c.cluster_probability)
        print '\t\tMedia: %s' % str(c.mean)
        print '\t\tStd: %s' % str(c.std)


def plot_ellipse(center, points, alpha, color):
    """
    Define el area del cluster como una elipse
    CONFIDENCE ELLIPSE
    """

    #  Covariance
    cov = np.cov(points, rowvar=False)
    
    eigenvalues, eigenvector = np.linalg.eigh(cov)
    order = eigenvalues.argsort()[::-1]
    eigenvector = eigenvector[:, order]

    angle = np.degrees(np.arctan2(*eigenvector[:, 0][::-1]))

    width, height = 4 * np.sqrt(eigenvalues[order])

    # Ellipse Object
    ellipse = Ellipse(xy=center, width=width, height=height, angle=angle, alpha=alpha, color=color)
    
    ax = plt.gca()
    ax.add_artist(ellipse)
    
    plt.savefig('grid_figure.pdf')

    return ellipse


def plot_results(clusters):
    plt.plot()
    new_points_cluster = [[] for i in range(NUM_CLUSTERS)]
#    print new_points_cluster
    for i, c in enumerate(clusters):
        # plot points
        x, y = zip(*[p.coordinates for p in c.points])
        for p in c.points:
            a = p.coordinates[0]
            b = p.coordinates[1]
            new_points_cluster[i].append(a)
            new_points_cluster[i].append(b)
        plt.plot(x, y, linestyle='None', color=COLORS[i], marker='.')
        # plot centroids
        plt.plot(c.mean[0], c.mean[1], 'o', color=COLORS[i],
                 markeredgecolor='k', markersize=10)
        # plot area
        plot_ellipse(c.mean, [p.coordinates for p in c.points], 0.2, COLORS[i])
#        print new_points_cluster
    puntos.append(new_points_cluster)
    plt.show()


def expectation_maximization(dataset, num_clusters, iterations):
    #densidad -> asignar 1+ distribuciones probabilisticas a un data set
    #PI = probabilidad de pertenecer a un cluster
    #C = Clusters
    #u = media de los puntos del cluster
    #X = dataset de puntos
    #sigma = desviacion estandar de los puntos
    
    # Lectura de data
    points = dataset_to_list_points(dataset)

    # Selecciono coordenada random de inicio [x,y]->
    initial = random.sample(points, num_clusters)

    # Creo N clusters iniciales
    clusters = [Cluster([p], len(initial)) for p in initial]
#    print clusters

    # Lista para saber los nuevos puntos de los clusters
    #devuelve lista de listas vacias
    new_points_cluster = [[] for i in range(num_clusters)]

    converge = False
    it_counter = 0
    #loop
    while (not converge) and (it_counter < iterations):
        # Expectation Step - prob de que un punto pertenezca a un cluster
        for p in points:
            i_cluster = get_expectation_cluster(clusters, p) #mayor probabilidad
            new_points_cluster[i_cluster].append(p)

        # Maximization Step - Maximizar la probabilidad de ocurrencia
        for i, c in enumerate(clusters):
            c.update_cluster(new_points_cluster[i], len(points))

        # Converge o no (por probabilidad)
        converge = [c.converge for c in clusters].count(False) == 0

        # Guarda los puntos de cada cluster, vacia de nuevo
        it_counter += 1
#        puntos.append(new_points_cluster)
        new_points_cluster = [[] for i in range(num_clusters)]

        # Print clusters status
        print_clusters_status(it_counter, clusters)

    print_resultados(clusters)
    plot_results(clusters)


#print puntos[0]
#x = 6.11
#y = 4.93
    
bandera = True

while (bandera):
    NUM_CLUSTERS = input("Ingrese el numero de gausianos: ")
    expectation_maximization(DATASET3, NUM_CLUSTERS, ITERATIONS)
    print "\nDetermine a que cluster pertenece un punto"
    x = float(input("Ingrese el punto X (dos decimales): "))
    y = float(input("Ingrese el punto Y (dos decimales): "))
    banderaX = False
    banderaY = False
    cluster = 0
    for i in range(0,len(puntos[0])):
        for j in range(0,len(puntos[0][i])):
            if(j%2 == 0):
                # Coordenada X
                if(round(puntos[0][i][j],2) == x):
    #                print "X Si pertenece al cluster ",i
                    banderaX = True
                    cluster = i
            else:
                if(round(puntos[0][i][j],2) == y):
    #                print "Y si pertenece al cluster ",i
                    cluster = i
                    banderaY  = True
    if(banderaX and banderaY):
        print "El punto ("+ str(x)+", "+str(y)+") pertenece al cluster " + str(cluster+1) + ", Color->"+str(COLORS[cluster])
    else:
        print "El punto ("+ str(x)+", "+str(y)+") NO pertenece a ningun cluster"
        
    salir = raw_input("Desea continuar? (y/n)" )
    salir = salir.lower()
    if (salir == "n"):
        bandera = False
        print "Gracias por utilizar el programa"
    elif(salir == "y"):
        print "Ok!"
#    else:
#        print "Dato inválido"