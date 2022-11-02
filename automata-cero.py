from importlib.resources import path
from webbrowser import get
import re

class cAutomata():
    path = ""
    def __init__(self,path):
        self.path = path
    get

    contador_general = 0

    def mostrar(self):
        archivo = open(self.path, 'r', encoding="utf-8")
        lineas2 = archivo.readlines()
        #print(len(lineas2))
        contadorLineas = 0
        contadorLineasgeneral = 0 
        banderacomen = False
        encontrado = False
        with open(self.path, 'r') as lineas:
        

            for l in lineas:
                #self.path = self.path + l
                contadorLineasgeneral = 1 + contadorLineasgeneral
                if(l.startswith('/*\n') or banderacomen == True or l.startswith('/*') or l.startswith('/*\t')):
                    print(l.strip())
                    banderacomen = True
                    contadorLineas = 1 + contadorLineas
                    if(l.endswith('*/\n') or l.endswith('*/') or l.endswith('*/\t')):
                        banderacomen = False
                        contadorLineas = 0
                        print("[Comentario multilinea]")
                    elif(banderacomen == True and len(lineas2) == contadorLineas):
                        print("[No cerro su comentario]")
                    elif(((l.endswith('*/\n') == False) or l.endswith('*/') == False) and (banderacomen==True) and (contadorLineasgeneral == len(lineas2))):
                        print("[No termino comentario]")
                    l = ""

                elif ((l.startswith('/*') or l.startswith('//')) and banderacomen == False):  
                    reconoceCaracter(l.rstrip())
                    l = ""
                elif (re.findall('^[a-zA-Z0-9]', l) or l.startswith('-') or l.startswith('+')):
                    reconocerVariable(l.rstrip())
                    l = ""
                else:
                    print('[No se reconocio nada]', l.rstrip())
                    l = ""

def reconoceCaracter(caracteres):
    #i = 0
    #while(i < len(caracteres)):
    estado = 1
    if ((caracteres[0]) == '/'):
        caracteres_nuevos = caracteres [1:]
        #print(caracteres_nuevos)
        estado = 2
        #i+=1
        if (((caracteres_nuevos[0]) == '*') and estado == 2):
            #caracteres_nuevos = caracteres_nuevos [1:]
            estado =  3
            #print(caracteres_nuevos)
            #i+=1
            if(caracteres[-1] == '*'):
                estado = 6
            if(estado == 3):
                #print (caracteres_nuevos)
                caracteres_nuevos = caracteres_nuevos [1:]
                for j in caracteres_nuevos:
                    if (j == '*'):
                        #print(j)
                        estado = 4
                        #i+=1
                        caracteres_nuevos = caracteres_nuevos [1:]
                        for k in caracteres_nuevos:
                            #print(k)
                            if (k == '*'):
                                estado = 4
                                #i+=1
                            if (k == '/'):
                                #print(k)
                                estado = 5
                                break
                            else:
                                if(k == caracteres_nuevos[-1]):
                                    #print(f"{contador} Linea analizada:  {caracteres} [NR]")
                                    estado = 6
                                    break
                                else:
                                    estado = 3
                                #i+=1
                    else:
                        if(j == caracteres_nuevos[-1]):
                                #print(f"{contador} Linea analizada:  {caracteres} [NR]")
                                estado = 6
                                break
                        else:
                            estado = 3
                        #i+=1
                    if (estado == 5):
                        break
                    if (estado == 6):
                        #estado = 6
                        break
            else:
                estado = 6
        else:
            if((caracteres_nuevos[0]) == '/'):
                estado=5
            else:
                estado = 6  
    else:
        estado = 6  
    #if (estado == 5) or ((caracteres[0]=='/') and (caracteres[1]=='/')):
    if estado == 5:
        print(f"Comentario analizado:  {caracteres} [R]")
    if estado == 6:
        print(f"Comentario no terminado:  {caracteres} [NR]")
        
def reconocerVariable(caracteres):
    #listDict = ['int','double','float']
    lista_pr = []
    lex = ''
    estado = 1
    if ((caracteres[0].isalpha()) and (caracteres[0] != '-') and (caracteres[0] != '+')):
        caracteres_nuevos = caracteres [1:]
        estado = 12
        for i in caracteres_nuevos:
            if((i.isalpha() or i.isnumeric() or (ord(i)) == 95) and estado != 13): #If condicional que resive palabras, numeros o giones bajos, mientras el estado no sea 3 #estado final convianado con ciclo
                estado = 12                                                          
            if((i.isalpha() or i.isnumeric() or (ord(i)) == 95)==False and estado != 12):
                estado = 13
            if((i.isalpha() or i.isnumeric() or (ord(i)) == 95)==False and (33 <= (ord(i)) and (ord(i)) <= 47) or (58 <= (ord(i)) and (ord(i)) <= 64 ) or (91 <= (ord(i)) and (ord(i)) <= 94 ) or (123 <= (ord(i)) and (ord(i)) <= 254 )):
                #captura todos los signos que no estaban contemplados 
                estado = 13

    elif(caracteres[0].isdigit() or caracteres.startswith('-') or caracteres.startswith('+')):
        estado = 1
        for caracter in caracteres.strip():
            if (estado == 1):
                
                if (caracter.isdigit() or caracter == '+' or caracter == '-'):
                    lex += caracter
                    estado = 2
                else:
                    estado = 6

            elif(estado == 2):

                if(caracter.isdigit()):
                    lex += caracter
                    estado = 2

                if(caracter == "."):
                    lex += caracter
                    estado = 3

                if(caracter == 'e' or caracter == 'E' ):
                    lex += caracter
                    estado = 4

            elif(estado == 3):
                if(caracter.isdigit() or caracter == '+' or caracter == '-'):
                    lex += caracter
                    estado = 3

                if(caracter == 'e' or caracter == 'E' ):
                    lex += caracter
                    estado = 4

            elif(estado == 4):
                if(caracter.isdigit() or caracter == '+' or caracter == '-'):
                    lex += caracter
                    estado = 5

            elif(estado == 5):
                if(caracter.isdigit()):
                    lex += caracter
                    estado = 5

            elif(estado == 6):
                break
        #print("Comparacion",caracteres,lex)
        validacionCadena(caracteres, lex)

    else:
        estado = 13

    if estado == 12:
        #with open(r"C:/Users/espar/Desktop/Reconocimiento-sintactico-estructural/palabras_reservadas.txt", 'r') as pr:
        reservadas = ["if", "else", "for", "while", "string", "int", "is", 
                    "double", "main", "False", "True", "string",
                    "doble","class","continue","return","elif", "float"]
        for palabra in caracteres.split():
            if palabra in reservadas:
                print(f"Palabra reservada [R] {palabra} ")
            else:
                print(f"Variable reconocida [NR] {palabra} ")
    if estado == 13:
        print(f"Variable no reconocida:  {caracteres} [NR]")

def validacionCadena(cadena, lex):
        if( cadena == lex):
            print(f'Exponente [R]: {lex}')
        else:
            print(f'Exponente [NR]: {cadena}')

#reconoceCaracter(str(input("Ingrese poblacion:")))
automataP = cAutomata("prueba_comentarios2.txt")
#automataP = cAutomata('C:/Users/espar/Desktop/Reconocimiento-sintactico-estructural/huachi/texto.txt')
#automataP = cAutomata("prueba_comentarios.txt")
automataP.mostrar()
