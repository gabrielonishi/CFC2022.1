'''

Camada Física da Computação, 2022.1
Script do servidor do Projeto 3

Gabriel Onishi
Jerônimo Afrange

'''
from enlace import *
from pacote import Packet
from mensagem import Message

import utils
import protocolo as protocol

import sys
import time
import numpy as np

serialName = "/dev/cu.usbmodem14101"  # Mac    (variacao de)
#serialName = "COM10"                     # Windows(variacao de)

def main():

    # *** *** *** *** *** *** *** *** *** *** ***
    #
    #
    #   CORRIGIR TIPO DE DADOS DE ENVIO
    #
    #
    # *** *** *** *** *** *** *** *** *** *** ***
    
    try:
        
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

        # loop de recepção de handshake
        while True:

            print("Aguardando o handshake...")

            rxBuffer, nRx = com1.getData(Packet.PACKET_SIZE)
            com1.rx.clearBuffer()
            print(utils.splitBytes(rxBuffer))

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
                print('\nHandshake fora dos conformes do datagrama\n')
                print(failure_message.packets[1].bytes_list)
                com1.sendData(failure_message.packets[1].sendable)
                com1.rx.clearBuffer()
                continue
            #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

            # verifica se o servidor indicou sucesso de transmissão --- --- ---
            valid, number_of_packets = protocol.validateHandshake(handshake_in)
            if valid:
                print('\nHandshake recebido, enviando de volta...\n')
                print(handshake_in.packets[1].bytes_list)
                com1.sendData(handshake_in.packets[1].sendable)
                com1.rx.clearBuffer()
                break
            #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        print("FIM DO HANDSHAKE")
        print("*"*50)

        '''

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
                    else:
                        com1.disable()
                        sys.exit()
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

        '''

        # Encerra comunicação
        print("\nCOMUNICAÇÃO ENCERRADA\n\n")
        com1.disable()

    except Exception as erro:
        print("\nops! :-\\\n")
        com1.disable()
        raise erro
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()