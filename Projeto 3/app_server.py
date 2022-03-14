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

# serialName = "/dev/cu.usbmodem14201"  # Mac    (variacao de)
serialName = "COM10"                     # Windows(variacao de)

def main():

    try:
        
        # Declaramos um objeto do tipo enlace com o nome "com" e ativa comunicação
        com1 = enlace(serialName)
        com1.enable()
        time.sleep(0.2)

        # Pegando o byte de sacrifício junto com a sujeira
        # Código cedido pelo Carareto

        print("Esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)

        # verbose de início de transmissão
        print("*"*50)
        print("INÍCIO DO RECEBIMENTO\n")

        while True:

            print("Aguardando o handshake...")

            rxBuffer, nRx = com1.getData(Packet.PACKET_SIZE)
            com1.clearBuffer()

            handshake_in = Message("in")
            success_message = Message("out", protocol.HANDSHAKE_DATA)
            failure_message = Message("out", protocol.PACKET_ERROR_DATA)
            reception_success = handshake_in.receive(rxBuffer)

            # em caso de handshake fora dos padrões do datagrama -- --- --- ---
            if not reception_success:
                print('Handshake fora dos conformes do datagrama\n')
                com1.sendData(failure_message.bytes)
                continue
            #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

            # verifica se o servidor indcou erro de transmissão --- --- --- ---
            elif validation_message == failure_message:
                print('Handshake inválido\n')
                com1.sendData(failure_message.bytes)
                continue
            #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

            # verifica se o servidor indicou sucesso de transmissão --- --- ---
            elif handshake_in == success_message:
                print('Handshake recebido, enviando de volta...')
                com1.sendData(success_message)
                break
            #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        print("\nAguardando pacotes...\n")
        
        while True: pass
    
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
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()