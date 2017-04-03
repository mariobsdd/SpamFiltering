from random import random, gauss
from matplotlib import pyplot as plt


NUMBER_OF_POINTS = 1000
MAXIMUM = 1.0
MINIMUM = -1.0
NUMBER_OF_CENTERS = 5
GENERATED_DISPERSSION = 0.04


def rtween(mi, ma):
    return mi + abs(ma - mi) * random()

points = []
centers = []

for i in xrange(NUMBER_OF_CENTERS):
    centers.append((
        rtween(MINIMUM, MAXIMUM),
        rtween(MINIMUM, MAXIMUM)
    ))

print "comenzar loop" 
generated_points = 0
while generated_points < NUMBER_OF_POINTS:
    print generated_points
    cx, cy = centers[generated_points % NUMBER_OF_CENTERS]
    px, py = (
        gauss(cx, GENERATED_DISPERSSION),
        gauss(cy, GENERATED_DISPERSSION)
    )

    if (MINIMUM < px < MAXIMUM) and (MINIMUM < py < MAXIMUM):
        points.append([px, py])

        generated_points += 1

figure = plt.figure()

plt.plot(*zip(*points), marker='o', color='r', ls='')

figure.show()

#raw_input()

for point in points:
    print "punto: ",point
