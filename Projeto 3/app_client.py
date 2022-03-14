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
import protocolo as protocol

import sys
import time
import numpy as np
import random

# Vamos convencionar que os dados do handshake serão [b'\xAB']
# Será convencionado também que o server deve simplemente espelhar o handshake
# Os dados do handshake deve ter no máximo 114 bytes
# SERIAL_PORT_NAME = "/dev/cu.usbmodem14201"  # Mac    (variacao de)
SERIAL_PORT_NAME = "COM10"                    # Windows(variacao de)

if len(HANDSHAKE_DATA) > 114: raise ValueError('Dados demais para o handshake')
if len(SERVER_INACTIVE_DATA) > 114: raise ValueError('Dados demais para sinalizar inatividade')

def main():

    try:
        
        # inicializando a porta
        com1 = enlace(SERIAL_PORT_NAME)
        com1.enable()
        time.sleep(.2)

        # enviando byte de sacrifício (necessário por conta de problemas de hardware)
        com1.sendData(b'00')
        time.sleep(1)
        
        '''
        HANDSHAKE

        Envio de uma mensagem conhecida pelo servidor para confirmar
        se ele está ativo e pronto para receber a mensagem

        Caso não se obtenha uma resposta com a mesma mensagem, como
        convencionado, em menos de 5 segundos, o usuário recebe uma
        mensagem: "Servidor inativo. Tentar novamente? S/N”
        
        Em caso de S, outra mensagem é executada
        Em caso de N, aplicação é encerrada
        
        '''

        # verbose de início de handshake
        print("*" * 50)
        print("INÍCIO DO HANDSHAKE\n")

        # criação do objeto Message do handshake e que será enviado pelo client
        handshake_out = Message("out", protocol.HANDSHAKE_DATA)
        handshake_success = False

        while not handshake_success:

            # Message de recebimento da resposta ao handshake
            handshake_in = Message("in")

            # Envio do handshake
            print("Enviando handshake")
            com1.sendData(handshake_out.bytes)
            time.sleep(0.1)
                
            # recepção da resposta
            print("Aguardando handshake de volta")
            rxBuffer, nRx = com1.getData(Packet.PACKET_SIZE)
            com1.rx.clearBuffer()

            # em caso de timeout    --- --- --- --- --- --- --- --- --- --- ---
            if rxBuffer is None:
                print("Hanshake timeout...")
                tryAgain = utils.tryAgainPrompt()
                if tryAgain: continue
                else: sys.exit()
            #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

            # em caso de recepção verifica se os bytes recebidos estão nos conformes
            reception_success = handshake_in.receive(rxBuffer)
            if not reception_success: print('O pacote recebido do servidor durante o handshake não está nos conformes')

            # verifica se os dados recebidos são os mesmos que foram enviados
            elif handshake_in == handshake_out:
                print("Handshake Recebido com sucesso!")
                print("\nFIM DO HANDSHAKE")
                print("*"*50)
                handshake_success = True

            # caso nada dê certo
            else: print("Erro de handshake")

        # verbose de fim de handshake
        print("\nFIM DO HANDSHAKE")
        print("*"*50)
        
        '''
        ENVIO DOS PACOTES
        
        '''

        # processamento da imagem
        img_bytes = open("./img_teste.png", 'rb').read()
        message = Message("out", img_bytes)
            
        # verbose de início de transmissão
        print("*"*50)
        print("INÍCIO DA TRANSMISSÃO\n")

        # mensagens de sucesso e falha
        success_message = Message("out", protocol.PACKET_RECEIVED_DATA)
        failure_message = Message("out", protocol.PACKET_ERROR_DATA)

        # loop de pacote em pacote
        for packet_id in range(1, message.number_of_packets + 1):

            # loop de tentativa
            while True:

                validation_message = Message("in")

                print("%d/%d... " % (packet_id, message.number_of_packets + 1), end='\t')

                packet = message.packets[packet_id]
                com1.sendData(packet.bytes)
                com1.tx.clearBuffer()
                time.sleep(0.1)

                # recepção da confirmação
                rxBuffer, nRx = com1.getData(Packet.PACKET_SIZE)
                com1.rx.clearBuffer()

                # em caso de timeout    --- --- --- --- --- --- --- --- --- --- ---
                if rxBuffer is None:
                    print("TIMEOUT")
                    tryAgain = utils.tryAgainPrompt()
                    if tryAgain: continue
                    else: sys.exit()
                #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

                # recepção da mensagem
                reception_success = validation_message.receive(rxBuffer)

                # em caso de mensagem fora dos padrões do datagrama --- --- --- ---
                if not reception_success:
                    print('CONFIRMAÇÃO FORA DOS PADRÕES')
                    continue
                #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

                # verifica se o servidor indcou erro de transmissão --- --- --- ---
                if validation_message == failure_message:
                    print('FALHA DE TRANSMISSÃO')
                    continue    # envia o pacote denovo
                #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

                # verifica se o servidor indicou sucesso de transmissão --- --- ---
                if validation_message == success_message:
                    print('OK')
                    break
                #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

                else: print('CONFIRMAÇÃO INVÁLIDA')

        # verbose de fim de transmissão
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