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

# --- --- --- --- --- --- --- CONFIGURAÇÕES  --- --- --- --- --- --- --- #
server_id = 1
client_id = 0

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
        local_imagem = "./Projeto 4 (Teste)/test_img.png"
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
            print("Esperando o servidor retornar")
            time.sleep(5)
            rxBuffer, nRx = com1.getData(Type2.SIZE)
            # Fazendo o decode do pacote do tipo 2 recebido
            packet = Packet.decode(rxBuffer)
            # Verifica se a mensagem recebida é do tipo 2 e se o id está certo
            if packet.message_type == 2 and packet.client_id == client_id: 
                inicia = True
                print("Eba! Mensagem do tipo 2 recebida")
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
            
            # envia o pacote com número {cont}
            print(f'Enviando pacote {cont}')
            com1.sendData(data_packet.sendable)
            time.sleep(0.1)

            # Definindo o início do timer de reenvio (tipo 1)
            timer1_start = time.time()
            # Definindo o início do timer de timeout (tipo 2)
            timer2_start = time.time()

            await_response = True
            
            # --- --- --- --- LOOP DE LEITURA DE RESPOSTA --- --- --- --- #

            while await_response == True:
                
                rxBuffer, nRx = com1.getData(size=Type4.SIZE)

                if(utils.getMessageType(rxBuffer)==2):
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
                        timer1_start = time.time()
                    # Testando Timeout
                    if timer2>20:
                        timeout_msg = Type5()
                        com1.sendData(timeout_msg.sendable)
                        com1.disable
                        print("\nTimeot!\nEncerrando COM")
                        sys.exit(':-(')
                    rxBuffer, nRx = com1.getData(size=Type6.SIZE)
                    # Vendo se recebeu mensagem do tipo 6
                    if utils.getMessageType(rxBuffer)==6:
                        print("Ops... Mandei um pacote errado")
                        # Lendo o pacote certo
                        error_packet = Packet.decode(rxBuffer)
                        cont = error_packet.expected_number
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