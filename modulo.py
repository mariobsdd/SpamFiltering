# -*- coding: utf-8 -*-
"""
Created on Sat Apr 01 19:58:17 2017

@author: mario
"""

from math import *
from collections import Counter

class DataFiltering:
        
    #separa mensajes con su tipo (ham y spam)
    def __init__(self,nombre):
        self.countHam = 0
        self.countSpam = 0
        self.clasificador = []
        self.data = [] #lista con toda la data (tipo + mensaje)
        self.msgtype = [] #lista con todos los tipos de mensajes del input
        self.message = [] #lista con todos los mensajes raw, sin el tipo
        archivo = open(nombre)        
        for linea in archivo:
            self.data.append(linea)
            tipo = linea.split("\t")[0].lower()
            mensaje = linea.split("\t")[1].lower()
            if (tipo == "ham"):
                self.countHam +=1
            elif (tipo == "spam"):
                self.countSpam +=1
            self.msgtype.append(tipo.lower())
            self.message.append(mensaje)
        print self.countHam,self.countSpam
#        print self.data
#        print self.message
            
    #funcion para preparacion de los datos
    #del input devuelve un string sin los signos/numeros, etc. 
    #lo que devuelve solo tiene letras minusculas y espacios
    def cleanInput(self,ascii):
        #el codigo ascii de las letras minusculas va del 97 al 122
        #entonces por cada elemento de la lista de asciis leidos quito todo lo que no este dentro de 97 a 122
        #or (i>=128 and i<=165) or (i>=48 and i<=57) #caracteres con tildes o letras raras y numeros
        #CASO ESPECIAL para : ','  '.' '-' que reemplazo por espacios
        letras = []
        cadenaLimpia = ""
        for i in ascii:
            if((i >= 44 and i<=47) or (i == 58) or (i==59) or (i == 63) or (i == 33)):
                i = 32
            if((i>=97 and i<=122) or (i == 32)):
                letras.append(chr(i)) #convierto otra vez a string
                cadenaLimpia += chr(i)
        #print letras
        return cadenaLimpia
    
    #funcion para quitar espacios, recibe como parametro una cadena de caracteres o string
    def quitarEspacios(self,cadena):
        cadenaSinEspacios = ""    
        cadena2 = cadena.split(" ")
        for i in cadena2:
            if(not(i == "")):
                cadenaSinEspacios = cadenaSinEspacios + i +" "
        return cadenaSinEspacios.strip() #quito el espacio del final
        
    def sanitizar(self,cleanInput,quitarEspacios, data):
        """
        El proceso de sanitizacion consiste en: pasar todo a ASCII
        ver criterio de aceptacion/rechazo de caracteres
        convertir de nuevo a string
        """
        sanitizado = []
        mtype = []
        for i in range(0,len(data)):
            try:
                raw = data[i].split("\t")[1].lower()
            except:
                raw = data[i].split("\t")[0].lower()
#            raw = data[i].split("\t")[1].lower()
            tipo = data[i].split("\t")[0].lower()
            ascii = [ord(c) for c in raw]
            clean = cleanInput(ascii)
            clean = quitarEspacios(clean)
            sanitizado.append(clean)
            mtype.append(tipo)
        return mtype,sanitizado
        

    def separateData(self, data, percentage):
        remaining_data = []
        preClassifiedData = []
        inserterted = False
        cantHam = 0
        cantSpam = 0
        for i in range(0,len(data)): 
          tipo = data[i].split("\t")[0].lower()
          if tipo == "ham":
            if (cantHam < (int)(round(self.countHam*percentage))):
              preClassifiedData.append(data[i])
              cantHam += 1
              inserterted = True
          elif tipo == "spam":
            if (cantSpam < (int)(round(self.countSpam*percentage))):
              preClassifiedData.append(data[i])
              cantSpam += 1
              inserterted = True
          if (inserterted == False):
            remaining_data.append(data[i])
          inserterted = False
        return preClassifiedData, remaining_data
        
    def getData(self, classifyData, p1, p2, p3):
        train, rem_data = classifyData(self.data, p1)
        cross_validation, rem_data = classifyData(rem_data, p2)
        test, rem_data = classifyData(rem_data, p3)
        return train, cross_validation, test
        
    def sortData(self,data,data_tipo):
        spams = []
        hams = []
        spams_tipos = []
        hams_tipo= []
        contSpam = 0
        contHam = 0
        for i in range(0,len(data)):
            if(data_tipo[i] == "spam"):
                spams.append(data[i])
                spams_tipos.append(data_tipo[i])
                contSpam +=1
            elif(data_tipo[i] == "ham"):
                hams.append(data[i])
                hams_tipo.append(data_tipo[i])
                contHam+=1
#        print "data: "+str(len(hams) + len(spams))
        data = []
        data_tipo = []
        #ordenamiento de la data en spam-ham
        for i in range(0,len(spams)):
            data.append(spams[i])
            data_tipo.append(spams_tipos[i])
            
        for i in range(0,len(hams)):
            data.append(hams[i])
            data_tipo.append(hams_tipo[i])
        return data,data_tipo,contSpam
        
    def setClasificador(self,data,data_tipo,contHam,contSpam, k):
        sinRepetir = []
        spamList = []
        hamList = []
        todas = []
        for i in range(0,len(data)):
            wordList = data[i].split(" ") #lista de palabras del mensaje
            if(data_tipo[i] == "spam"):
                for word in wordList:
                    if word not in sinRepetir:
                        sinRepetir.append(word)
                    spamList.append(word)
                    todas.append(word)
            elif(data_tipo[i] == "ham"):
                for word in wordList:
                    if(word not in sinRepetir):
                        sinRepetir.append(word)
                    hamList.append(word)
                    todas.append(word)
            
        frecSpam = Counter()
        frecHam = Counter()
        for item in spamList: 
            frecSpam = frecSpam + Counter(item.split())
        for item in hamList: 
            frecHam = frecHam + Counter(item.split())
            
#        clasificador = []
        for i in sinRepetir:
            temp = []
            probDadoSpam = float(frecSpam[i]+k)/float(len(spamList) + (k*len(sinRepetir)))
            probDadoHam = float(frecHam[i]+k)/float(len(hamList) + (k*len(sinRepetir)))
            temp.append(i)
            temp.append(probDadoHam)
            temp.append(probDadoSpam)
            self.clasificador.append(temp)

        return self.clasificador
        
    def outputBayes(self,data,probSpam,probHam):
        lista = []
        probs = []
        prob = 0.0
        for i in data: #cada mensaje
            lista = i.split(" ")
            probAuxHam = 1.0;
            probAuxSpam = 1.0;
            for j in lista: #cada palabra del mensaje
                for l in self.clasificador: #cada palabra dentro del clasificador
                    if(l[0] == j):
                        probAuxHam *= l[1]
                        probAuxSpam *= l[2]
            a = float(probAuxSpam*probSpam)
            b =  float(float(probAuxSpam*probSpam)+float(probAuxHam*probHam))
            if(b == 0.0):
                b = 1
            prob = a/b
            if (prob>=0.5 and prob<=1.0):
                probs.append("spam "+str(prob))
    #        elif(b >= 1 or prob>1):
    #            probs.append("Error! "+str(prob))
            else:
                probs.append("ham "+str(prob))
        return probs
            
        