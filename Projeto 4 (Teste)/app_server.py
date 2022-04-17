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
import os
import sys

# --- --- --- --- --- --- --- CONFIGURAÇÕES  --- --- --- --- --- --- --- #

# identificadores
server_id = 1
client_id = 0
# nome do arquivo de log
filename =  "./Server.txt"
# nome do arquivo recebido
received_file = "./img_recebida.png"
# garantindo que não existam esses arquivos
if os.path.exists(filename):
    os.remove(filename)
if os.path.exists(received_file):
    os.remove(received_file)
data_list = []

# serialName = "/dev/cu.usbmodem14201
serialName = "COM3"  
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
        sacrificio = False
        while not sacrificio:
            rxBuffer, nRx = com1.getData(1)
            if rxBuffer != b'\xAB':
                sacrificio = True
        com1.rx.clearBuffer()
        time.sleep(.1)
        print("OK")
        print("-- --"*15)

        # --- --- --- --- --- --- LOOP DE HANDSHAKE --- --- --- --- --- --- #
        ocioso = True
        print("Iniciando protocolo de handhake")
        print("Aguardando mensagem")
        while ocioso:
            raw_head, nRx = com1.getData(Packet.HEAD_SIZE)
            rop_size = Packet.getROPSize(raw_head)
            if rop_size is not False:
                raw_rop, nRx = com1.getData(rop_size)
                raw_packet = raw_head + raw_rop
            else:
                raw_packet = raw_head

            # Recriando o datagrama a partir do que foi recebido
            handshake = Packet.decode(raw_packet)
            if handshake and isinstance(handshake, Type1):
                utils.writeLog(filename, handshake, "receb")
                if handshake.server_id == server_id:
                    print("Eba! Handshake recebido com ID certo")
                    ocioso = False
                    # Salvando a quantidade total de pacotes
                    ammount = handshake.ammount
                else: print("Recebi uma mensagem, mas não é pra mim")

        # Enviando mensagem do tipo 2 (resposta do handshake)
        handshake_response = Type2(client_id=client_id)
        print("Enviando mensagem do tipo 2")
        com1.sendData(handshake_response.sendable)
        time.sleep(0.1)
        utils.writeLog(filename, handshake_response, "envio")

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
            rop_size = Packet.getROPSize(raw_head)
            if rop_size is not False:
                raw_rop, nRx = com1.getData(rop_size)
                raw_packet = raw_head + raw_rop
            else:
                raw_packet = raw_head
            packet = Packet.decode(raw_packet)
            if packet:
                utils.writeLog(filename, packet, "receb")
                if isinstance(packet, Type3) and packet.number==cont:
                    print(f'Mensagem {cont} OK')
                    print("Enviando mensagem de confirmação")
                    confirm = Type4(last_received=cont)
                    com1.sendData(confirm.sendable)
                    time.sleep(0.1)
                    utils.writeLog(filename, confirm, "envio")
                    cont += 1
                    # Adicionando isso à mensagem final
                    data_list.append(raw_packet[Packet.HEAD_SIZE:-Packet.EOP_SIZE])
                elif isinstance(packet, Type3):
                    print("Recebi um pacote de dados não esperado")
                    print("Enviando mensagem de relato de problema")
                    error_msg = Type6(expected_number=cont)
                    com1.sendData(error_msg.sendable)
                    time.sleep(0.1)
                    utils.writeLog(filename, error_msg, "envio")
                elif isinstance(packet, Type5):
                    print("Recebi uma mensagem de timeout")
                    print("Encerrando a comunicação")
                    com1.disable()
                    sys.exit(':-(')
            else:           
                timer1 = time.time()-timer1_start
                timer2 = time.time()-timer2_start
                if timer2>20:
                    ocioso = True
                    # Criando mensagem de timeout
                    timeout = Type5()
                    com1.sendData(timeout.sendable)
                    time.sleep(0.1)
                    utils.writeLog(filename, timeout, "envio")
                    com1.disable()
                    print(":-(")
                elif timer1 > 2:
                    packet = Type4(last_received=cont)
                    com1.sendData(packet.sendable)
                    time.sleep(0.1)
                    utils.writeLog(filename, packet, "envio")
                    timer1_start = time.time()
        
        print("Sucesso!")
        with open(received_file, "wb") as file:
            file.write(np.asarray(data_list))

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()