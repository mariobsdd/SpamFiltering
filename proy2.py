# -*- coding: utf-8 -*-
"""
Created on Sat Apr 01 19:43:20 2017

@author: mario
"""

from modulo import *
from math import *

classifier = DataFiltering("test_corpus.txt")
tipo, clean = classifier.sanitizar(classifier.cleanInput,classifier.quitarEspacios,classifier.data)


train, cross, test = classifier.getData(classifier.separateData, 0.8, 0.1, 0.1)
print "Data Separada!"

train_tipo, train = classifier.sanitizar(classifier.cleanInput,classifier.quitarEspacios,train)
cv_tipo, cross = classifier.sanitizar(classifier.cleanInput,classifier.quitarEspacios,cross)
test_tipo, test = classifier.sanitizar(classifier.cleanInput,classifier.quitarEspacios,test)
print "Data Sanitizada!"


#TRAINING DATA
train,train_tipo,contSpam = classifier.sortData(train,train_tipo)
    
k = 1

contHam = fabs(len(train)-contSpam)
probSpam = float(contSpam + k)/float(len(train) + (k*2))
probHam = float(contHam + k)/float(len(train) + (k*2))
print probSpam,probHam

clasificador = classifier.setClasificador(train,train_tipo,contHam,contSpam, k)

probabilidades = classifier.outputBayes(train,probSpam,probHam)
#print probabilidades

archivo = open("outputTrain.txt",'w')
Rspam = 0
Rham = 0
Pspam = 0
Pham = 0
FPham = 0
FPspam = 0
for i in range(0,len(probabilidades)):
    archivo.write(train_tipo[i]+"\t"+probabilidades[i]+"\n")
    if(train_tipo[i] == 'spam'):
        Rspam +=1
    elif(train_tipo[i] == 'ham'):
        Rham +=1
    if((probabilidades[i].split(" ")[0] == train_tipo[i]) and (train_tipo[i] == 'spam')):
        Pspam +=1
    elif((probabilidades[i].split(" ")[0] == train_tipo[i]) and (train_tipo[i] == 'ham')):
        Pham +=1
    if((probabilidades[i].split(" ")[0] != train_tipo[i]) and (train_tipo[i] == 'spam')):
        #todos los que yo dije que eran ham y eran SPAM
        FPspam +=1
    elif((probabilidades[i].split(" ")[0] != train_tipo[i]) and (train_tipo[i] == 'ham')):
        #todos los que yo dije que eran SPAM y eran HAM
        FPham +=1

archivo.close()
print "TRAINING DATA"
print "%Exito Spam: ",float(Pspam)/float(Rspam)
print "%Exito Ham: ",float(Pham)/float(Rham)
print "******Confussion Matrix - Training Data******"
print "\t\tPredictedSPAM\t\tPredictedHAM"
print "RealSPAM\t"+str(Pspam)+"\t\t\t\t"+str(FPspam)
print "RealHAM\t\t"+str(FPham)+"\t\t\t\t"+str(Pham)
exito = float(Pspam+Pham)/float(Rham + Rspam)
print "Porcentaje de Exito: ",exito
print "************************"

#CROSS VALIDATION
cross,cv_tipo,contSpam = classifier.sortData(cross,cv_tipo)
    
k = 1

contHam = fabs(len(cross)-contSpam)
probSpam = float(contSpam + k)/float(len(cross) + (k*2))
probHam = float(contHam + k)/float(len(cross) + (k*2))
print probSpam,probHam

clasificador = classifier.setClasificador(cross,cv_tipo,contHam,contSpam, k)

probabilidades = classifier.outputBayes(cross,probSpam,probHam)
#print probabilidades

archivo = open("outputCrossValidation.txt",'w')
Rspam = 0
Rham = 0
Pspam = 0
Pham = 0
FPham = 0
FPspam = 0
for i in range(0,len(probabilidades)):
    archivo.write(cv_tipo[i]+"\t"+probabilidades[i]+"\n")
    if(cv_tipo[i] == 'spam'):
        Rspam +=1
    elif(cv_tipo[i] == 'ham'):
        Rham +=1
    if((probabilidades[i].split(" ")[0] == cv_tipo[i]) and (cv_tipo[i] == 'spam')):
        Pspam +=1
    elif((probabilidades[i].split(" ")[0] == cv_tipo[i]) and (cv_tipo[i] == 'ham')):
        Pham +=1
    if((probabilidades[i].split(" ")[0] != cv_tipo[i]) and (cv_tipo[i] == 'spam')):
        #todos los que yo dije que eran ham y eran SPAM
        FPspam +=1
    elif((probabilidades[i].split(" ")[0] != cv_tipo[i]) and (cv_tipo[i] == 'ham')):
        #todos los que yo dije que eran SPAM y eran HAM
        FPham +=1

archivo.close()
print "CROSS VALIDATION DATA"
print "%Exito Spam: ",float(Pspam)/float(Rspam)
print "%Exito Ham: ",float(Pham)/float(Rham)
print "******Confussion Matrix - CROSS VALIDATION Data******"
print "\t\tPredictedSPAM\t\tPredictedHAM"
print "RealSPAM\t"+str(Pspam)+"\t\t\t\t"+str(FPspam)
print "RealHAM\t\t"+str(FPham)+"\t\t\t\t"+str(Pham)
exito = float(Pspam+Pham)/float(Rham + Rspam)
print "Porcentaje de Exito: "+str(exito)+", Para un K = "+str(k)
print "************************"
#PARA K = 1,    0.996415770609 | 0.982078853047
#Para K = 0.8,  0.994623655914
#Para K = 0.5,  0.991039426523
#para K = 2,    0.992831541219
#Para K = 0.9, 1.1,1.2, me dio a misma K que con K =1
#CON TESTING:::
#PARA K = 1.5,  0.987455197133
#"""
#*******************************************************************************
#TESTING SAMPLE FROM INPUT.TXT
archivo = open("input.txt")
testing = []
for line in archivo:
    testing.append(line)
archivo.close()
#CROSS VALIDATION
test,test_tipo,contSpam = classifier.sortData(test,test_tipo)
    
k = 2

contHam = fabs(len(test)-contSpam)
probSpam = float(contSpam + k)/float(len(test) + (k*2))
probHam = float(contHam + k)/float(len(test) + (k*2))
print probSpam,probHam

clasificador = classifier.setClasificador(test,test_tipo,contHam,contSpam, k)
tipo_testing, testing = classifier.sanitizar(classifier.cleanInput,classifier.quitarEspacios,testing)
probabilidades = classifier.outputBayes(testing,probSpam,probHam)
#print probabilidades

archivo = open("output.txt",'w')
Rspam = 0
Rham = 0
Pspam = 0
Pham = 0
FPham = 0
FPspam = 0
for i in range(0,len(probabilidades)):
    archivo.write(probabilidades[i].split(" ")[0]+"\t"+testing[i]+"\n")
#    if(test_tipo[i] == 'spam'):
#        Rspam +=1
#    elif(test_tipo[i] == 'ham'):
#        Rham +=1
#    if((probabilidades[i].split(" ")[0] == test_tipo[i]) and (test_tipo[i] == 'spam')):
#        Pspam +=1
#    elif((probabilidades[i].split(" ")[0] == test_tipo[i]) and (test_tipo[i] == 'ham')):
#        Pham +=1
#    if((probabilidades[i].split(" ")[0] != test_tipo[i]) and (test_tipo[i] == 'spam')):
#        #todos los que yo dije que eran ham y eran SPAM
#        FPspam +=1
#    elif((probabilidades[i].split(" ")[0] != test_tipo[i]) and (test_tipo[i] == 'ham')):
#        #todos los que yo dije que eran SPAM y eran HAM
#        FPham +=1

archivo.close()
#print "TESTING DATA"
#print "%Exito Spam: ",float(Pspam)/float(Rspam)
#print "%Exito Ham: ",float(Pham)/float(Rham)
#print "******Confussion Matrix - CROSS VALIDATION Data******"
#print "\t\tPredictedSPAM\t\tPredictedHAM"
#print "RealSPAM\t"+str(Pspam)+"\t\t\t\t"+str(FPspam)
#print "RealHAM\t\t"+str(FPham)+"\t\t\t\t"+str(Pham)
#exito = float(Pspam+Pham)/float(Rham + Rspam)
#print "Porcentaje de Exito: "+str(exito)