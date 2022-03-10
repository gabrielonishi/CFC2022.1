'''

Camada Física da Computação, 2022.1
Script de recepção de comandos do Projeto 2

Gabriel Onishi
Jerônimo Afrange

'''

from sys import byteorder
from enlace import *
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