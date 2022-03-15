

import math
import numpy as np

from pacote import Packet

class Message():
    '''

    Classe que representa uma mensagem a ser enviada dividida em pacotes

    Propriedades:
    - data_list: dados brutos a serem enviados (lista de bytes separados)
    - packets: dicionário de instâncias de Packet que compõe a mensagem
    - data_size: tamanho dos dados úteis a serem enviados
    - total_size: tamanho de todos os pacotes somados
    - number_of_packets: quantidade de pacotes que compõem a mensagem
    - is_complete: se a mensagem está completa ou não
    - type: "in" ou "out" (a ser preenchida ou já preenchida)
    - last_received: último pacote recebidoo, False para mensagem completa

    '''

    def __init__(self, message_type, data=[]):
        '''
        Inicializa um objeto Message

        Parâmetros:
        - message_type: tipo da mensagem, "in" ou "out"
        - data: lista de bytes dos dados não separados
        
        '''

        # amarra os argumentos à instância de Message
        self.data_list = data
        self.type = message_type

        # determina se a mensagem está completa ou não
        if self.type == 'in':
            self.last_received = 0
            self.is_complete = False
        elif self.type == 'out':
            self.last_received = False
            self.is_complete = True
        else:
            raise ValueError('Tipo de mensagem inválido, use "in" ou "out" somente')

        # extrai as especificações dos pacotes
        max_data = Packet.MAX_DATA
        payload_size = Packet.PAYLOAD_SIZE

        # verifica a validade dos argumentos
        if len(data) > max_data: raise ValueError('Mensagem grande demais')

        # calcula a quantidade de datagramas necessários
        number_of_packets = math.ceil(len(data) / payload_size)
        if number_of_packets > Packet.MAX_PACKETS: raise ValueError('Impossível enviar tantos pacotes')
        self.number_of_packets = number_of_packets

        # divide os dados brutos em pacotes  --- --- --- --- --- --- --- --- --- --- ---
        # e adiciona os bytes dos pacotes à lista de bytes
        self.packets = dict()
        self.bytes_list = list()

        for i in range(number_of_packets):

            # intervalo para extrair dos dados brutos
            from_index = i * payload_size
            to_index = (i + 1) * payload_size

            # extrai o intervalo e cria um datagrama com o payload
            payload = data[from_index:to_index]
            packet = Packet(self, i + 1, payload)

            # adiciona o datagrama à lista de datagramas e preenche a lista de bytes
            self.packets[i + 1] = packet
            self.bytes_list += packet.bytes_list

        #-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        # define demais propriedades
        self.total_size = len(self.bytes_list)
        self.data_size = len(self.data)


    def receivePacket(self, raw_packet):
        '''
        Adiciona um pacote recebido à mensagem
        Retorna False se o pacote recebido for inválido

        Parâmetros:
        - raw_packet: lista de bytes do pacote recebido
        
        '''

        if self.is_complete: raise Exception('Essa mensagem já está completa')

        # decodifica o pacote e retorna False se houver falhas
        received_packet = Packet.decode(self, raw_packet)
        if received_packet is None: return False

        # verifica se o recebido é o próximo do último recebido
        if received_packet.number != self.last_received + 1: return False

        # incrementa o last received
        self.last_received = received_packet.number

        # verifica se a mensagem foi completada
        if self.last_received == self.number_of_packets: self.is_complete = True

        # adiciona os dados do pacote aos dados totais da mensagem
        self.packets[received_packet.number] = received_packet
        self.bytes_list += received_packet.bytes_list
        self.data_list += received_packet.data

        # atualiza demais propriedades
        self.number_of_packets = received_packet.ammount
        self.total_size += Packet.PACKET_SIZE
        self.data_size += received_packet.data_size
        
        return True


    def __eq__(self, other):
        ''' Overload do comparador de igualdade '''

        # verifica se other é Message também
        if not isinstance(other, Message): return False

        # renomeia propriedades
        size = self.number_of_packets

        # verifica o tamanho de ambas as instâncias
        if self.data_size != other.data_size: return False

        # percorre todos os pacotes de ambas as instâncias
        equal = True
        for i in range(1, number_of_packets + 1):
            equal = equal and (self.packets[i] == other.packets[i])
            if not equal: return False

        return True



