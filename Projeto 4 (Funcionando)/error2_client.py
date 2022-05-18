"""
Arquivo para simulação de erro 2: Transmissão com erro na ordem dos pacotes enviados pelo client.
Troca pacote 3 com 4 na hora de enviar

Deve ser rodado com app_server.py normalmente

OBS: ID do cliente - 0; ID do servidor - 1
"""

from enlace import *
import utils
from datagrams import *
import time
import numpy as np
import math
from datetime import datetime
import sys
import os

# --- --- --- --- --- --- --- CONFIGURAÇÕES  --- --- --- --- --- --- --- #
server_id = 1
client_id = 0
filename = "./Projeto 4 (Funcionando)/Client.txt"
if os.path.exists(filename):
    os.remove(filename)

# serialName = "/dev/cu.usbmodem14201
serialName = "COM4"

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #

def main():

    try:
        # --- --- --- --- INICIALIZAÇÃO E BYTE DE SACRIFÍCIO --- --- --- --- #

        # Declaramos um objeto do tipo enlace com o nome "com" e ativa comunicação
        com1 = enlace(serialName)
        com1.enable()
        
        # Envio de um byte de sacrifício
        print("-- --"*15)
        print("Enviando byte de sacrifício")
        com1.sendData(b'00')
        time.sleep(1)
        print("OK")
        print("-- --"*15)

        # Dados a serem transmitidos (bytes da imagem "test_img.png")
        local_imagem = "./Projeto 4 (Funcionando)/test_img.png"
        raw_data = open(local_imagem, 'rb').read()
        # Transformando dados em uma lista de bytes
        data = utils.splitBytes(raw_data)
        data_size = len(data)
        ammount =  math.ceil(data_size / Packet.MAX_PAYLOAD_SIZE)

        # --- --- --- --- --- --- LOOP DE HANDSHAKE --- --- --- --- --- --- #

        inicia = False
        
        while inicia == False:
            # Criando um datagrama do tipo 1 (handshake)
            handshake = Type1(server_id=server_id, ammount=ammount)
            print("Enviando Mensagem do Tipo 1")
            com1.sendData(handshake.sendable)
            time.sleep(0.1)

            # Escrevendo arquivo
            utils.writeLog(filename=filename, packet=handshake, direction="envio")

            print("Esperando o servidor retornar")
            time.sleep(5)

            raw_head, nRx = com1.getData(Packet.HEAD_SIZE)
            rop_size = Packet.getROPSize(raw_head)
            if rop_size is not False:
                raw_rop, nRx = com1.getData(rop_size)
                raw_packet = raw_head + raw_rop
            else:
                raw_packet = raw_head

            # Usando decode pra criar um objeto packet
            packet = Packet.decode(raw_packet)

            # Vendo se de fato recebeu um objeto do tipo packet
            if packet is not False:
                # Escrevendo log
                utils.writeLog(filename=filename, packet=packet, direction="receb")
                # Verifica se a mensagem recebida é do tipo 2 e se o id está certo
                if isinstance(packet, Type2):
                    if packet.client_id == client_id:
                        inicia = True
                        print("Eba! Responderam o handshake!")
                    else: print("Recebi uma mensagem do tipo 2, mas não é pra mim\nEnviando de novo")
                else: print("Recebi uma mensagem de tipo inesperado\nEnviando de novo")
            else: 
                print("Ops... Servidor não respondeu\nEnviando de novo")
        
        # --- --- --- --- --- --- LOOP DE ENVIO --- --- --- --- --- --- #
        print("-- --"*15)
        print("Vamos começar :)\n")

        cont = 1
        
        while cont<=ammount:
            # intervalo para extrair dos dados brutos
            from_index = (cont-1) * Packet.MAX_PAYLOAD_SIZE
            to_index = cont * Packet.MAX_PAYLOAD_SIZE

            # extrai o intervalo e cria um Packet com os dados (definidos lá atrás)
            packet_data = data[from_index:to_index]
            data_packet = Type3(ammount=ammount, number=cont, data=packet_data)



            # ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ #
            # AQUI ESTÁ A SIMULAÇÃO DO ERRO - invertemos pacotes 3 e 4 de ordem
            if(cont==3):
                from_index = (3) * Packet.MAX_PAYLOAD_SIZE
                to_index = 4 * Packet.MAX_PAYLOAD_SIZE

                packet_data = data[from_index:to_index]
                data_packet = Type3(ammount=ammount, number=4, data=packet_data)
            if(cont==4):
                from_index = (2) * Packet.MAX_PAYLOAD_SIZE
                to_index = 3 * Packet.MAX_PAYLOAD_SIZE

                packet_data = data[from_index:to_index]
                data_packet = Type3(ammount=ammount, number=3, data=packet_data)
            # ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ ~~~ #



            print(f'Enviando pacote {cont}')
            com1.sendData(data_packet.sendable)
            time.sleep(0.1)
            utils.writeLog(filename=filename, packet=data_packet, direction="envio")

            # Definindo o início do timer de reenvio (tipo 1)
            timer1_start = time.time()
            # Definindo o início do timer de timeout (tipo 2)
            timer2_start = time.time()

            await_response = True
            
            # --- --- --- --- LOOP DE LEITURA DE RESPOSTA --- --- --- --- #

            while await_response == True:
                
                # Lendo o head
                raw_head, nRx = com1.getData(Packet.HEAD_SIZE)
                rop_size = Packet.getROPSize(raw_head)
                if rop_size is not False:
                    raw_rop, nRx = com1.getData(rop_size)
                    raw_packet = raw_head + raw_rop
                else:
                    raw_packet = raw_head
                
                received_packet = Packet.decode(raw_packet)
                
                # Vendo se recebeu mensagem de confirmação e se o número do pacote era o experado
                if received_packet and isinstance(received_packet, Type4) and received_packet.last_received == cont:
                    # Escrevendo no log
                    utils.writeLog(filename=filename, packet=received_packet, direction="receb")
                    print("Mensagem Recebida!")
                    cont += 1
                    await_response = False
                else:
                    # Definindo timer
                    timer1 = time.time() - timer1_start
                    timer2 = time.time() - timer2_start

                    # Testando reenvio
                    if timer1>5:
                        print("Acho que não recebeu...")
                        print("Tentando enviar de novo")
                        com1.sendData(data_packet.sendable)
                        time.sleep(0.1)
                        utils.writeLog(filename, data_packet, "envio")
                        timer1_start = time.time()
                    
                    # Testando Timeout
                    if timer2>20:
                        timeout_msg = Type5()
                        com1.sendData(timeout_msg.sendable)
                        time.sleep(0.1)
                        utils.writeLog(filename, timeout_msg, "envio")
                        com1.disable
                        print("\nTimeot!\nEncerrando COM")
                        sys.exit(':-(')
                   
                    # Vendo se recebeu mensagem do tipo 6
                    if received_packet and isinstance(received_packet, Type6):
                        utils.writeLog(filename, received_packet, "receb")
                        print("Ops... Mandei um pacote errado")
                        # Lendo o pacote certo
                        cont = received_packet.expected_number
                        # Refazendo o pacote t3
                        from_index = (cont-1) * Packet.MAX_PAYLOAD_SIZE
                        to_index = cont * Packet.MAX_PAYLOAD_SIZE
                        packet_data = data[from_index:to_index]
                        packet = Type3(ammount=ammount, number=cont, data=packet_data)
                        # envia o pacote
                        print("Reenviando o pacote")
                        print(f"Enviando pacote {cont}")
                        com1.sendData(packet.sendable)
                        time.sleep(0.1)
                        utils.writeLog(filename, packet, "envio")
                        timer1_start = time.time()
                        timer2_start = time.time()
                        await_response = False
            
        print("SUCESSO!!!")
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()