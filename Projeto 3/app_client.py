'''

Camada Física da Computação, 2022.1
Script de envio de comandos do Projeto 2

Gabriel Onishi
Jerônimo Afrange

'''
from enlace import *
from pacote import Packet
from mensagem import Message
import utils

import time
import numpy as np
import random

# serialName = "/dev/cu.usbmodem14201"  # Mac    (variacao de)
serialName = "COM10"                    # Windows(variacao de)

def main():

    try:
        # Processamento da imagem
        img_bytes = open("./img_teste.png", 'rb').read()
        
        #Inicializando a porta
        com1 = enlace(serialName)
        com1.enable()
        time.sleep(.2)

        # Enviando byte de sacrifício (necessário por conta de problemas de hardware)
        com1.sendData(b'00')
        time.sleep(1)
        
        # ENVIANDO INFORMAÇÕES

        """
        PARTE I: HANDSHAKE
        Envio de uma mensagem conhecida pelo servidor para confirmar
        se ele está ativo
        Caso não se obtenha uma resposta com *a mesma mensagem* em
        menos de 5 segundos, o usuário recebe uma mensagem: "Servidor 
        inativo. Tentar novamente? S/N”
        
        Em caso de S, outra mensagem é executada

        Em caso de N, aplicação é encerrada
        
        """

        print("*"*50)
        print("INÍCIO DO HANDSHAKE\n")
        # Vamos convencionar que o payload de handshake será b'\xAB'
        handshake = Packet(number=1, ammount=1, payload=[b'\xAB'])
        handshake_success = False
        while not handshake_success:
            print("Enviando handshake")
            com1.sendData(handshake.bytes)
            time.sleep(0.1)
            print("Aguardando handshake de volta")
            rxBuffer, nRx = com1.getData(128)
            mensagem_hs = Message()
            handshake = mensagem_hs.receive(rxBuffer)
            if(handshake.data == [b'\xAB']):
                print("Handshake Recebido com sucesso!")
                print("Enviando package de volta")
                com1.sendData(handshake.bytes)
                time.sleep(0.1)
                print("\nFIM DO HANDSHAKE")
                print("*"*50)
                handshake_success = True
            elif(handshake.data == b'\xAA')

        print("\nFIM DO HANDSHAKE")
        print("*"*50)
        
        # # Gerando o txBuffer, ou a fila de dados que serão transferidos
        # txBuffer = comandos_enviados

        # #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        # tamanho_txBuffer = len(txBuffer)
            
        # verbose de início de transmissão
        print("*"*50)
        print("INÍCIO DA TRANSMISSÃO\n")
        # print(f"Lista de comandos enviados: {comandos_enviados}")
        print(f'{n} comandos no total')
        # print("Enviando dados (%d bytes)\n" % tamanho_txBuffer)

        # início da transmissão
        # com1.sendData(np.asarray(txBuffer))     # envio dos dados
        # time.sleep(0.1)

        print("FIM DA TRANSMISSÃO")
        print("*"*50)
        print("INÍCIO DO RECEBIMENTO\n")

        # RECEBENDO INFORMAÇÕES DE VOLTA

        # rxBuffer, nRx = com1.getData(1)

        # Encerra comunicação
        print("\nFIM DO RECEBIMENTO")
        print("*"*50)
        print("\nCOMUNICAÇÃO ENCERRADA\n\n")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()