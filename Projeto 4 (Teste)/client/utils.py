from numpy import byte
from datagrams import *

def splitBytes(data):
    """
    Transforma um conjunto de dados em uma lista de bytes
    """
    split_data = [data[i:i + 1] for i in range(0, len(data), 1)]
    result = list()
    for data in split_data:
        result.append(bytes(data))
    return result

def tryAgainPrompt():

    while True:

        answer = input("Tentar novamente? S/N\n")
        if answer.upper() == "N": return False
        elif answer.upper() == "S": return True
        else: print("Não entendi.\n")

local_imagem = "./Projeto 4/test_img.png"
txBuffer = open(local_imagem, 'rb').read()
print(txBuffer)
print(splitBytes(txBuffer))