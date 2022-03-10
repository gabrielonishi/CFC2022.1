'''

Camada Física da Computação, 2022.1
Script de envio de comandos do Projeto 2

Gabriel Onishi
Jerônimo Afrange

'''
from enlace import *

import time
import numpy as np
import random

# serialName = "/dev/cu.usbmodem14201"  # Mac    (variacao de)
serialName = "COM10"                    # Windows(variacao de)

"""
Comando 1: 00 FF 00 FF (comando de 4 bytes)
Comando 2: 00 FF FF 00 (comando de 4 bytes)
Comando 3: FF (comando de 1 byte)
Comando 4: 00 (comando de 1 byte)
Comando 5: FF 00 (comando de 2 bytes) 
Comando 6: 00 FF (comando de 1 bytes)

"""

def main():

    try:
        # ENVIANDO INFORMAÇÕES
        # Gerando os comandos a serem enviados aleatóriamente
        n = random.randint(10,30)
        comandos_enviados = []

        #Dicionário de comandos
        comandos_parsed = [[b"\x00",b"\xFF",b"\x00",b"\xFF"], [b"\x00",b"\xFF", b"\xFF",b"\x00"], [b"\xFF"], [b"\x00"], [b"\xFF", b"\x00"], [b"\x00", b"\xFF"]]

        for i in range(n):
            comando_aleatorio = comandos_parsed[random.randint(0,5)]
            tamanho_do_comando = len(comando_aleatorio).to_bytes(1, byteorder='big')
            comandos_enviados.append(tamanho_do_comando)
            for byte in comando_aleatorio:
                comandos_enviados.append(byte)
        
        # Adicionando um tail que informa que o pacote acabou
        comandos_enviados.append(b'\x11')
        
        # A estrutura dos dados enviados é:
        # Tamanho do comando -> Comando -> Tamanho do Comando -> Comando ... -> b'\x11'

        # Sabemos que o dado que informa o tamanho do comando é sempre 1, então podemos lê-lo sem problemas

        # Declaramos um objeto do tipo enlace com o nome "com" e ativa comunicação
        com1 = enlace(serialName)
        com1.enable()
        time.sleep(.2)

        # Enviando byte de sacrifício (necessário por conta de problemas de hardware)
        com1.sendData(b'00')
        time.sleep(1)
        
        # Gerando o txBuffer, ou a fila de dados que serão transferidos
        txBuffer = comandos_enviados

        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        tamanho_txBuffer = len(txBuffer)
            
        # verbose de início de transmissão
        print("*"*50)
        print("INÍCIO DA TRANSMISSÃO\n")
        print(f"Lista de comandos enviados: {comandos_enviados}")
        print(f'{n} comandos no total')
        print("Enviando dados (%d bytes)\n" % tamanho_txBuffer)

        # início da transmissão
        com1.sendData(np.asarray(txBuffer))     # envio dos dados
        time.sleep(0.1)

        print("FIM DA TRANSMISSÃO")
        print("*"*50)
        print("INÍCIO DO RECEBIMENTO\n")

        # RECEBENDO INFORMAÇÕES DE VOLTA

        # Sabemos com certeza que o número de comandos varia de 10 a 30

        rxBuffer, nRx = com1.getData(1)
        n_recebidos = int.from_bytes(rxBuffer, byteorder='big')
        
        if (rxBuffer==b'\xaa' or n_recebidos==170):
            print("ERRO: Timeout")
        elif (n != n_recebidos):
            print(f'ERRO: \n Comandos Enviados - {n} \n Comandos Recebidos - {n_recebidos}')
        elif 10<n_recebidos<=30:
            print(f'SUCESSO: Número de Comandos: {n}')

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