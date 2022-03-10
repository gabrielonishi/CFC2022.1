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

        # Pegando o byte de sacrifício junto com a sujeira
        # Código cedido pelo Carareto

        time.sleep(0.2)
        print("Esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)

        # verbose de início de transmissão
        print("*"*50)
        print("INÍCIO DO RECEBIMENTO\n")

        """
        Exemplo de Mensagem Normal Enviada
        [b'\x04', b'\x00', b'\xff', b'\x00', b'\xff', b'\x02',
         b'\x00', b'\xff', b'\x02', b'\xff', b'\x00', b'\x01',
         b'\x00', b'\x02', b'\x00', b'\xff', b'\x02', b'\x00', 
         b'\xff', b'\x04', b'\x00', b'\xff', b'\xff', b'\x00', 
         b'\x01', b'\xff', b'\x04', b'\x00', b'\xff', b'\xff', 
         b'\x00', b'\x02', b'\x00', b'\xff', b'\x02', b'\x00', 
         b'\xff', b'\x02', b'\xff', b'\x00', b'\x02', b'\xff', 
         b'\x00', b'\x01', b'\x00', b'\x01', b'\x00', b'\x04', 
         b'\x00', b'\xff', b'\x00', b'\xff', b'\x11']
        """

        # Começando a coleta de dados reais
        comandos_recebidos = []
        print("Esperando tamanho")

        # Lendo primeiro dado fora do loop para ter certeza que não é b'x11' (mensagem vazia)
        rxBuffer, nRx = com1.getData(1)         # Primeiro dado é sempre a respeito do tamanho do próximo dado (tem 1 byte)
        comandos_recebidos.append(rxBuffer)
        # Loop para ler dados segundo o tamanho de cada
        while rxBuffer != b'\x11':
            # Transformando o tamanho de bits para int
            tamanho = int.from_bytes(rxBuffer, byteorder="big")
            # Pegando o comando seguinte a partir de seu tamanho
            rxBuffer, nRx = com1.getData(tamanho)
            comandos_recebidos.append(rxBuffer)
            # Pegando o tamanho da próxima mensagem
            rxBuffer, nRx = com1.getData(1)
            comandos_recebidos.append(rxBuffer)
        print(f'Dados recebidos: {comandos_recebidos}')
        
        n_recebidos = int((len(comandos_recebidos) - 1)/2)

        print(f"Número de instruções recebidas: {n_recebidos}\n")

        # Enviando o número de instruções de volta

        txBuffer = bytes([n_recebidos])

        print("FIM DO RECEBIMENTO")
        print("*"*50)
        print("INÍCIO DA TRANSMISSÃO\n")
        
        # CASO 1: DANDO CERTO

        print(f"Mandando: \n{txBuffer}")
        com1.sendData(np.asarray(txBuffer))

        # CASO 2: DANDO ERRADO
        
        # print("Mandando: b'\x02'")
        # com1.sendData(np.asarray(b'\x02'))
        
        # CASO 3: DANDO TIMEOUT

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