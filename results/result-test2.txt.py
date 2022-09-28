def main():
    # nombre del algoritmo:TEST2
    #BLOQUE VARIABLES
    suma  = 0 #tipo: ENTERO
    stop  = 0 #tipo: BOOLEANO
    n  = 0 #tipo: ENTERO
    #FIN BLOQUE VARIABLES, INICIO PROGRAMA
    
    suma = 0
    stop = 1
    n = 4
    for  i in range(0 ,n+1,1):
    
        if  stop != 0 :
            if  i==n/2 :
                stop = 0
            else:
                suma = suma+i+2
            #FIN_SI
            
        #FIN_SI
        
    i+=1
     #FIN DESDE
    
    print(i,suma,stop,n)
main()