Program to translate pseudocode into a executable python script

- Problems:
    - Translates all symbols, even those in quotes, for example, it might replace ```"o"``` for ```"or"``` inside a string, most of the symbols are not a problem because they are uppercase. 
    - This program simply translates pseudocode into equivalent python, it does not validate it, for example, you could have 2 "VARIABLE" blocks or even variables outside that block and it wouldn't throw an error, similarly, if there are errors in the pseudocode they will be translated into python
- Support:
    - Symbols
        - It can translate basically every pseudocode symbol , for a more exhaustive list  of each symbol and it's equivalent in python check file main.py lines 116-132
        - Code blocks
            -It currently supports ```"VARIABLES","SI"(IF),"CASO"(CASE),"MIENTRAS"(WHILE) AND "DESDE"(FOR)``` 
        - Missing
            -Support for ```Struct``` and other complex variable types
            -Support for ```"LEER(x)" (x = input())```
            -Support for nesting (yet), a few code changes are needed in the indent calculating and block calculating code
            
- Usage:
  - Download the repository and run ```main.py``` with python, it will translate the pseudocode inside the file ```text.txt```,save into ```result.py``` and try to run it, if it doesn't work automatically, you can open the resulting code to get insight into what might be the problem (and open a github issue if it is a bug)

