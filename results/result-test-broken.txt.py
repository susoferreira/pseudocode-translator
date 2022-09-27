def main():
    # nombre del algoritmo:SUMAR
    #BLOQUE VARIABLES
    x  = 0 #tipo: REAL
    y  = 0 #tipo: ENTERO
    #FIN BLOQUE VARIABLES, INICIO PROGRAMA
    
    while  x < 10 :
        for  i  in range( 0 , 20 +1, 7 ):
            print(i)
            x = x+1
        i +=1
        
    #FIN_MIENTRAS
    
    if  5==4 :
        print("cosa 1")
        x = 5
        x = x % 2
        
    else:
        print("cosa 2")
    #FIN_SI
    
    if  5==4 :
        print("cosa 3")
    else:
        print("cosa 4")
    #FIN_SI
    
    if  5==4 :
        print("cosa 5")
    else:
        print("cosa 6")
    #FIN_SI
    
    if  x*3  == 1:print("X POR 3 ES 1")
    elif  x*3  == 2:print("X POR 3 ES 2")
    elif  x*3  == 3:print("X POR 3 ES 3")
    elif  x*3  == 4:print("X POR 3 ES 4")
    elif  x*3  == 5:print("X POR 3 ES 5")
    else:
        print("X POR 3 ES UN VALOR INESPERADO")
    #FIN_CASO
    
    
main()