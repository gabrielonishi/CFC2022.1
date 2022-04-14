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

server_id = 1
client_id = 0
result_img = []

# serialName = "/dev/cu.usbmodem14201
serialName = "COM4"                 

def main():

    try:
        
        # Declaramos um objeto do tipo enlace com o nome "com" e ativa comunicação
        com1 = enlace(serialName)
        com1.enable()

        # Pegando o byte de sacrifício junto com a sujeira
        # Código cedido pelo Carareto
        print("Esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)

        ocioso = True
        while ocioso:
            rxBuffer, nRx = com1.getData(Type1.SIZE)
            if(utils.getMessageType(rxBuffer==1)):
                handshake = utils.decode(rxBuffer)
                if handshake.id == server_id:
                    ocioso = False
                    ammount = handshake.ammount
            time.sleep(1)
        
        handshake_response = Type2(client_id=client_id)
        com1.sendData(handshake_response)
        cont = 1
        while(cont<=ammount):
            timer1_start = time.time()
            timer2_start = time.time()
            raw_head, nRx = com1.getData(Packet.HEAD_SIZE)
            head_elements = utils.readType3Head(raw_head=raw_head)
            
            if head_elements["message_type"] == 3:
                raw_payload_and_eop, nRx = com1.getData(head_elements["payload_size"]+Packet.EOP_SIZE)
                payload_and_eop_list = utils.splitBytes(raw_payload_and_eop)
                if (payload_and_eop_list[-4]== b'\xAA' and payload_and_eop_list[-3]== b'\xBB' and payload_and_eop_list[-2]== b'\xCC' and payload_and_eop_list[-1]== b'\xDD'):

            else:
                time.sleep(1)
                
            
                

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()