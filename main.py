#!/usr/bin/python3
import os
import sys
from block import BlockDescriptor, BlockTranslator
from src.Parser import Parser
from settings import settings

def __init__():
    file=sys.argv[1]
    text=open(file,"r").read()
    parser = Parser(text)
    settings["indent_size"] =parser.indent_length
    parser.parse()
    result=parser.syntax_pass_output()
    

    with open("./results/result-{}.py".format(file.split("/")[-1]),"w") as r:
        r.write(result)
    print("el resultado se ha guardado en result.py")
    print("intentando ejecutar automáticamente...")
    print("si no se ejecuta automáticamente puedes revisar el archivo result.py manualmente e intentar ejecutarlo")
    print("\n"*3)
    os.system("python ./results/result-{}.py".format(file.split("/")[-1]))

__init__()
