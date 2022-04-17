from numpy import byte
from datagrams import *
from datetime import datetime

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

def writeLog(filename:str, packet:Packet, direction:str):
    """
    Escreve em file segundo instruções do enunciado
    Parâmetros:
    - filename: nome do arquivo gerado
    - packet: pacote processado
    - direction: DEVE SER "envio" ou "receb", fala se a mensagem é de envio ou recebimento
    """
    file = open(filename, "a")
    # Abre file no modo append (a)
    # Pacotes com o tipo 3 são os únicos com log diferente
    if isinstance(packet, Type3):
        file.write(f'{datetime.today()} /{direction} /3 /{packet.size} /{packet.number} /{packet.ammount}\n')
    else:
        file.write(f'{datetime.today()} /{direction} /{int.from_bytes(packet.message_type, byteorder="big")} /{packet.size}\n')
    file.close()
    
