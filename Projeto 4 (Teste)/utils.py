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

def getMessageType(raw_packet:list):
    """
    Recebe um pacote inteiro e devolve o tipo de mensagem do pacote
    Criado para aumentar eficiência computacional
    """
    bytes_list = splitBytes(raw_packet)
    head = bytes_list[ : Packet.HEAD_SIZE]
    message_type = int.from_bytes(head[0], byteorder="big")
    return(message_type)

def readType3Head(raw_head:list):
    """
    Recebe o head de um pacote e devolve um dicionário com os seguintes parâmetros:
    - message_type: tipo da mensagem
    - ammount: quantidade total de pacotes a serem enviados
    - number: número do pacote que envia (começa do 1)
    - payload_size: tamanho do payload
    """
    h = splitBytes(raw_head)
    return ({"message_type": int.from_bytes(h[0],byteorder="big"), 
             "ammount":int.from_bytes(h[3],byteorder="big"), 
             "number":int.from_bytes(h[4],byteorder="big"), 
             "payload_size":int.from_bytes(h[5],byteorder="big")})

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