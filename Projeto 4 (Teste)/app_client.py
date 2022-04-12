"""
Arquivo para aplicação do lado do cliente

OBS: ID do cliente - 0; ID do servidor - 1
"""

from enlace import *
import utils
from datagrams import *
import time
import numpy as np
import math
import sys

server_id = 1
client_id = 0

# serialName = "/dev/cu.usbmodem14201
serialName = "COM4"                 

def main():

    try:
        
        # Declaramos um objeto do tipo enlace com o nome "com" e ativa comunicação
        com1 = enlace(serialName)
        com1.enable()
        
        # Envio de um byte de sacrifício
        print("-- --"*50)
        print("Enviando byte de sacrifício")
        com1.sendData(b'00')
        time.sleep(1)
        print("OK")
        print("-- --"*50)

        # Dados a serem transmitidos (bytes da imagem "test_img.png")
        local_imagem = "./Projeto 4 (Teste)/test_img.png"
        raw_data = open(local_imagem, 'rb').read()
        # Transformando dados em uma lista de bytes
        data = utils.splitBytes(raw_data)
        data_size = len(data)
        ammount =  math.ceil(data_size / Packet.MAX_PAYLOAD_SIZE)

        inicia = False
        
        while inicia == False:
            print("Enviando o Handshake")
            handshake = Type1(server_id=server_id, ammount=ammount).sendable
            com1.sendData(handshake)
            time.sleep(5)
            rxBuffer, nRx = com1.getData(Type2.size)
            com1.rx.clearBuffer
            packet = utils.decode(rxBuffer)
            if packet.message_type ==2: inicia = True
        
        # loop de fragmentação
        cont = 1
        while cont<=ammount:
            # intervalo para extrair dos dados brutos
            from_index = (cont-1) * Packet.MAX_PAYLOAD_SIZE
            to_index = cont * Packet.MAX_PAYLOAD_SIZE

            # extrai o intervalo e cria um Packet com os dados
            packet_data = data[from_index:to_index]
            packet = Type3(ammount=ammount, number=cont, data=packet_data)
            
            # envia o pacote
            com1.sendData(packet.sendable)
            time.sleep(0.1)

            # define o tempo base para os timers 1 e 2
            timer1_start = time.time()
            timer2_start = time.time()

            await_response = True
            
            while await_response == True:
                # tenta pegar a mensagem do 
                rxBuffer, nRx = com1.getData(size=Type4.SIZE)

                if(utils.getMessageType(rxBuffer)==2):
                    cont += 1
                    timer1 = time.time() - timer1_start
                    timer2 = time.time() - timer2_start
                    if timer1>5:
                        com1.sendData(packet.sendable)
                        timer1_start = time.time()
                    if timer2>20:
                        timeout_msg = Type5()
                        com1.sendData(timeout_msg.sendable)
                        com1.disable
                        sys.exit(':-(')
                    rxBuffer, nRx = com1.getData(size=Type6.SIZE)
                    if utils.getMessageType(rxBuffer):
                        error_msg = utils.decode(rxBuffer)
                        cont = error_msg.expected_number
                        from_index = (cont-1) * Packet.MAX_PAYLOAD_SIZE
                        to_index = cont * Packet.MAX_PAYLOAD_SIZE

                        # extrai o intervalo e cria um Packet com os dados
                        packet_data = data[from_index:to_index]
                        packet = Type3(ammount=ammount, number=cont, data=packet_data)
                        # envia o pacote
                        com1.sendData(packet.sendable)
                        time.sleep(0.1)
                        timer1_start = time.time()
                        timer2_start = time.time()
                        await_response = False

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()