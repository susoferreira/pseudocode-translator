Programa para traducir pseudocódigo a un script ejecutable de python.

## Uso:
  - Descarga el repositorio y ejecuta ```main.py file_name``` con  python, traducirá el pseudocódigo dentro del archivo, lo guardará en la carpeta ```results/```  e intentará ejecutarlo, si no funciona automáticamente, puede abrir el código resultante para obtener una idea de cuál podría ser el problema (y abrir un problema de github si es un bug).
  - ###### Solo windows

    - Arrastrar cualquier archivo de texto a ```main.py``` en vez de ejecutarlo desde la consola de comandos debería funcionar (abrir con...)



## Importante
- Funciona todo menos los operadores <= y >= y posiblemente algún símbolo más
- ~~El bloque hacer... mientras aún no está implementado~~

### Problemas:

- Traduce todos los símbolos, incluso los que están entre comillas, por ejemplo, podría reemplazar ```"o"```por ```"or"``` dentro de una cadena, la mayoría de los símbolos no son un problema porque están en mayúsculas.
  - ​	(```o``` e ```y``` actualmente están deshabilitados debido a esos problemas, puede volver a habilitarlos descomentando las líneas correspondientes en la clase ```Parser``` en ```main.py``` ) 
- Este programa simplemente traduce el pseudocódigo a python equivalente, no lo valida, por ejemplo, podría tener 2 bloques "VARIABLES" o incluso variables fuera de ese bloque y no arrojaría un error, de manera similar, si hay errores en el pseudocódigo se traducirán a python

### Soporte:

- ##### Simbolos
    - Puede traducir básicamente todos los símbolos de pseudocódigo (también admite comentarios de estilo c), para obtener una lista más exhaustiva de cada símbolo y su equivalente: ```main.py``` lines 116-132
- ##### Bloques de codigo
    - Actualmente soporta  ```"VARIABLES","SI"(IF),"CASO"(CASE),"MIENTRAS"(WHILE),"DESDE"(FOR), y HACER...MIENTRAS(DO..WHILE) ```
    - Anidado de bloques de código (Hasta que se pruebe lo contrario) 

- ##### Falta
    - Soporte para  ```Struct``` y otros tipos complejos de variables
    - Soporte para ```"LEER(x)" (x = input())```

    -~~Soporte para el anidado de bloques de código~~

