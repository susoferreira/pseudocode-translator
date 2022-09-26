Program to translate pseudocode into a executable python script

## Usage:
  - Download the repository and run ```main.py file_name``` with python, it will translate the pseudocode inside the file, save it into  ```results/``` folder and try to run it, if it doesn't work automatically, you can open the resulting code to get insight into what might be the problem (and open a github issue if it is a bug)

  - ###### Windows only

    - Dragging and dropping any text file to ```main.py``` (open with) should work instead of opening it from the console 

## Important

Sometimes the program will break if you start a code block the line immediately after the ```INICIO``` keyword  (like in ```tests/test-broken.txt```), just leaving an empty line (like in ```tests/test.txt```) should work

### Problems:

- Translates all symbols, even those in quotes, for example, it might replace ```"o"``` for ```"or"``` inside a string, most of the symbols are not a problem because they are uppercase.
  - ​	(```o``` and ```y``` are currently disabled because of those problems, you can re-enable them by uncommenting the correspondent lines in class ```Parser``` in ```main.py``` ) 
- This program simply translates pseudocode into equivalent python, it does not validate it, for example, you could have 2 "VARIABLE" blocks or even variables outside that block and it wouldn't throw an error, similarly, if there are errors in the pseudocode they will be translated into python

### Support:

- ##### Symbols
    - It can translate basically every pseudocode symbol (also supports c style comments) , for a more exhaustive list  of each symbol and it's equivalent in python check file ```main.py``` lines 116-132
- ##### Code blocks
    -It currently supports ```"VARIABLES","SI"(IF),"CASO"(CASE),"MIENTRAS"(WHILE) AND "DESDE"(FOR)``
    - Code blocks nesting (until proven otherwise) 

- ##### Missing
    -Support for ```Struct``` and other complex variable types
    -Support for ```"LEER(x)" (x = input())```
    -~~Support for nesting (yet), a few code changes are needed in the indent calculating and block calculating code~~

