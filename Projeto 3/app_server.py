'''

Camada Física da Computação, 2022.1
Script de recepção de comandos do Projeto 2

Gabriel Onishi
Jerônimo Afrange

'''
from enlace import *
from pacote import Packet
from mensagem import Message

import utils
import protocolo as protocol

from sys import byteorder
import time
import numpy as np

serialName = "/dev/cu.usbmodem14101"  # Mac    (variacao de)
#serialName = "COM10"                     # Windows(variacao de)

def main():
    
    # Declaramos um objeto do tipo enlace com o nome "com" e ativa comunicação
    com1 = enlace(serialName)
    com1.enable()
    time.sleep(0.2)

    # Pegando o byte de sacrifício junto com a sujeira
    # Código cedido pelo Carareto

    print("Esperando 1 byte de sacrifício")
    rxBuffer, nRx = com1.getData(1, 1e12)
    com1.rx.clearBuffer()
    time.sleep(.1)

    # verbose de início de transmissão
    print("*"*50)
    print("INÍCIO DO RECEBIMENTO\n")

    while True:

        print("Aguardando o handshake...")

        rxBuffer, nRx = com1.getData(Packet.PACKET_SIZE)
        com1.rx.clearBuffer()

        # em caso de timeout
        if rxBuffer is None:
            print("Timeout")
            tryAgain = utils.tryAgainPrompt()
            if tryAgain: continue
            else: sys.exit()

        handshake_in = Message("in")
        failure_message = Message("out", protocol.PACKET_ERROR_DATA)
        reception_success = handshake_in.receivePacket(rxBuffer)

        # em caso de handshake fora dos padrões do datagrama -- --- --- ---
        if not reception_success:
            print('Handshake fora dos conformes do datagrama\n')
            com1.sendData(failure_message.bytes)
            com1.rx.clearBuffer()
            continue
        #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        # verifica se o servidor indicou sucesso de transmissão --- --- ---
        valid, number_of_packets = protocol.validateHandshake(handshake_in)
        if valid:
            print('Handshake recebido, enviando de volta...\n')
            com1.sendData(handshake_in.bytes)
            com1.rx.clearBuffer()
            break
        #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

    print("FIM DO HANDSHAKE")
    print("*"*50)

    print()
    print("*"*50)
    print("RECEBENDO PACOTES\n")

    message_in = Message("in")

    error_response = Message("out", protocol.PACKET_ERROR_DATA)
    success_response = Message("out", protocol.PACKET_RECEIVED_DATA)
    
    # loop de recebimento de pacotes
    for packet_id in range(1, ammount + 1):

        while True:

            print("%d/%d... " % (packet_id, ammount), end='\t')

            # recebimento dos dados
            rxBuffer, nRx = com1.getData(Packet.PACKET_SIZE)
            com1.rx.clearBuffer()

            # em caso de timeout    --- --- --- --- --- --- --- --- --- --- ---
            if rxBuffer is None:
                print("TIMEOUT")
                tryAgain = utils.tryAgainPrompt()
                if tryAgain: continue
                else: sys.exit()
            #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

            # validação da mensagem
            reception_success = validation_message.receivePacket(rxBuffer)

            # em caso de pacote fora dos padrões do datagrama --- --- --- ---
            if not reception_success:
                print('PACOTE FORA DOS PADRÕES')
                continue
            #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

            # verifica se o servidor indicou sucesso de transmissão --- --- ---
            else:
                print('OK')
                break
            #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

    # verbose de fim de transmissão
    print("FIM DA TRANSMISSÃO")
    print("*"*50)




    # Verificar primeiro xAA pra ter certeza que é o pacote de handshake
    # if rxBuffer==b'\xAA': 
        

    # RECEBENDO DADOS

    # rxBuffer, nRx = com1.getData(1)       
    
    # Enviando o número de instruções de volta

    # txBuffer = bytes([n_recebidos])

    print("FIM DO RECEBIMENTO")
    print("*"*50)
    print("INÍCIO DA TRANSMISSÃO\n")
    
    # print(f"Mandando: \n{txBuffer}")
    # com1.sendData(np.asarray(txBuffer))

    # time.sleep(11)

    print("FIM DA TRANSMISSÃO\n")
    print("*"*50)

    # Encerra comunicação
    print("\nCOMUNICAÇÃO ENCERRADA\n\n")
    com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()