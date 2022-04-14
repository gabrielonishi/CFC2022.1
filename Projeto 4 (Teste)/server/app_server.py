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

# --- --- --- --- --- --- --- CONFIGURAÇÕES  --- --- --- --- --- --- --- #
server_id = 1
client_id = 0
result_img = []
# serialName = "/dev/cu.usbmodem14201
serialName = "COM4"  
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #               

def main():

    try:
        # --- --- --- --- INICIALIZAÇÃO E BYTE DE SACRIFÍCIO --- --- --- --- #

        # Declaramos um objeto do tipo enlace com o nome "com" e ativa comunicação
        com1 = enlace(serialName)
        com1.enable()

        # Pegando o byte de sacrifício junto com a sujeira
        # Código cedido pelo Carareto
        print("-- --"*15)
        print("Esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        print("OK")
        print("-- --"*15)

        # --- --- --- --- --- --- LOOP DE HANDSHAKE --- --- --- --- --- --- #
        ocioso = True
        print("Iniciando protocolo de hanshake")
        while ocioso:
            print("Aguardando mensagem")
            rxBuffer, nRx = com1.getData(Type1.SIZE)
            # Recriando o datagrama a partir do que foi recebido
            handshake = Packet.decode(rxBuffer)
            if handshake.message_type==1:
                if handshake.server_id == server_id:
                    print("Eba! Handshake recebido com ID certo")
                    ocioso = False
                    # Salvando a quantidade total de pacotes
                    ammount = handshake.ammount
                else: print("Recebi uma mensagem, mas não é pra mim")
            else: print("Recebi uma mensagem, mas não é um handshake")
            time.sleep(1)
        
        # Enviando mensagem do tipo 2 (resposta do handshake)
        handshake_response = Type2(client_id=client_id)
        print("Enviando mensagem do tipo 2")
        com1.sendData(handshake_response)

        # --- --- --- --- --- --- LOOP DE RECEBIMENTO --- --- --- --- --- --- #
        print("-- --"*15)
        print("Vamos começar :)\n")
        cont = 1

        print("Aguardando mensagem do servidor")
        while(cont<=ammount):
            # Definindo o início do timer de reenvio (tipo 1)
            timer1_start = time.time()
            # Definindo o início do timer de timeout (tipo 2)
            timer2_start = time.time()
            raw_head, nRx = com1.getData(Packet.HEAD_SIZE)
            head_elements = Packet.readType3Head(raw_head=raw_head)
            
            # Checando se a mensagem é do tipo 3 mesmo
            if head_elements["message_type"] == 3:
                # Pegando o payload e EOP a partir do tamanho do payload dado pelo head
                raw_PLEOP, nRx = com1.getData(head_elements["payload_size"]+Packet.EOP_SIZE)
                PLEOP_list = utils.splitBytes(raw_PLEOP)
                # Checando se o número está correto e se tem EOP
                if cont == head_elements["number"] and (PLEOP_list[-4]== b'\xAA' and PLEOP_list[-3]== b'\xBB' and PLEOP_list[-2]== b'\xCC' and PLEOP_list[-1]== b'\xDD'):
                    print(f'Mensagem {cont} OK')
                    # Enviando mensagem do tipo 4
                    print("Enviando mensagem de confirmação")
                    confirm = Type4(last_received=cont)
                    com1.sendData(confirm.sendable)
                    cont += 1
                else:
                    # Mandando mensagem de erro
                    print("Recebi um pacote não esperado")
                    print("Enviando mensagem de relato de problema")
                    error_msg = Type6(expected_number=cont)
            # Se não recebeu uma mensagem do tipo 3
            else:
                # eu acho que tem que colocar essa parte na interface física
                # caso contrário vai ficar no getdata pra sempre
                time.sleep(1)
                timer1 = time.time()-timer1_start
                timer2 = time.time()-timer2_start
                if timer2>20:
                    ocioso = True
                    # Criando mensagem de timeout
                    timeout = Type5()
                    com1.sendData(timeout.sendable)
                    com1.disable
                    print(":-(")
                elif timer1 > 2:
                    # Enviando mensagem do tipo 4
                    # --- --- --- NAO ENTENDI --- --- ---
                    response = Type4(last_received=cont)
                    timer1_start = time.time()
                
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()