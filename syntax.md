sustituciones:
declaración de variables

empieza con VARIABLES
nome_variable2 : tipo_variable2 --> nome_variable2=0 (no hace falta especificar tipo en python)
constantes: no existe ningún método para crear constantes en python
subrango: --> (?)
enumerado --> diccionario con valores numericos
asignacion : <- --> =

traducciones de operadores:
 y --> and
 o --> or
 MOD --> %
 DIV --> //
 ^ --> **
 = --> ==
 no --> not
 <> --> !=


control de flujo:
     CONTINUAR --> continue
     INTERRUMPIR --> break



 funciones:
 ESCRIBIR(texto) = print(texto)
 LEER(var) -> var =input()

 estructuras condicionales

 SI (LOGICA) ENTONCES
     X
 SI_NO
     Y
 ===========
 if condicion:
     X
 else:
     Y


 SI (LOGICA) ENTONCES
     X
 SI_NO (LOGICA) ENTONCES
     Y
 =========================
 if(logica):
     x
 elif:
     y

CASO <expresión> SEA
     <valor1>: < INSTRUCIÓNS 1>
     <valor2>: < INSTRUCIÓNS 2>
     ..........
     [SI_NO]: < INSTRUCIÓNS SI_NO>
FIN_CASO

======================

 var = expresión
 if var==valor1:
     instruccions 1
 elif var==valor2:
     instruccions 2
 else:
     instruccions_si_no



 DESDE <variable><-<inicio> HASTA <FINAL> PASO <paso> HACER 
     INSTRUCCIONES
 FIN_DESDE
 ======================
     for <variable> in range(<inicio>,<final>,<paso>)

 MIENTRAS <expresión_lóxica> HACER
     <INSTRUCIÓNS>
FIN_MIENTRAS
     while(<expresion_lóxica>):