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
import sys

import time
import numpy as np
import random

# Vamos convencionar que os dados do handshake serão [b'\xAB']
# Será convencionado também que o server deve simplemente espelhar o handshake
# Os dados do handshake deve ter no máximo 114 bytes
# SERIAL_PORT_NAME = "/dev/cu.usbmodem14201"  # Mac    (variacao de)
SERIAL_PORT_NAME = "COM10"                    # Windows(variacao de)
HANDSHAKE_DATA = [b'\xAB']
SERVER_INACTIVE_DATA = [b'\xAA']

if len(HANDSHAKE_DATA) > 114: raise ValueError('Dados demais para o handshake')
if len(SERVER_INACTIVE_DATA) > 114: raise ValueError('Dados demais para sinalizar inatividade')

def main():

    try:
        # Processamento da imagem
        img_bytes = open("./img_teste.png", 'rb').read()
        
        #Inicializando a porta
        com1 = enlace(SERIAL_PORT_NAME)
        com1.enable()
        time.sleep(.2)

        # Enviando byte de sacrifício (necessário por conta de problemas de hardware)
        com1.sendData(b'00')
        time.sleep(1)
        
        # ENVIANDO INFORMAÇÕES

        """
        PARTE II: HANDSHAKE
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

        # criação do objeto Message do handshake que será enviado pelo client
        dummy_inactive_message = Message("out", SERVER_INACTIVE_DATA)
        handshake_out = Message("out", HANDSHAKE_DATA)
        handshake_success = False

        while not handshake_success:

            # Message de recebimento da resposta ao handshake
            handshake_in = Message("in")

            # Envio do handshake
            print("Enviando handshake")
            com1.sendData(handshake_out.bytes)
            time.sleep(0.1)
                
            # recepção da resposta e verificação da integridade dos dados
            print("Aguardando handshake de volta")
            rxBuffer, nRx = com1.getData(Packet.PACKET_SIZE)
            reception_success = handshake_in.receive(rxBuffer)
            if not reception_success: print('O pacote recebido do servidor durante o handshake não está nos conformes')

            # verifica se os dados recebidos são os mesmos que foram enviados
            elif handshake_in == handshake_out:
                print("Handshake Recebido com sucesso!")
                print("\nFIM DO HANDSHAKE")
                print("*"*50)
                handshake_success = True

            # verifica se o servidor está inativo e pede input do usuário
            elif handshake_in == dummy_inactive_message:

                valid_answer = False
                while not valid_answer:

                    answer = input("Servidor inativo. Tentar novamente? S/N")

                    if answer == "N":
                        print("Encerrando aplicação :(")
                        valid_answer = True
                        sys.exit()

                    elif answer == "S": valid_answer = True
                    else: print("Não entendi")

            # caso nada dê certo
            else: print("Erro de handshake")
        

        '''
        PARTE III: FRAGMENTAÇÃO
        Dividir a mensagem bruta em vários pacotes de 128 bytes

        '''

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