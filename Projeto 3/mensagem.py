'''
Arquivo criado para armazenar a classe de Datagrama

'''

import math
import utils

from pacote import Packet

class Message():
    '''

    Classe que representa uma mensagem a ser enviada dividida em pacotes

    Propriedades:
    - data: dados brutos a serem enviados
    - packets: lista de instâncias de Packet que compõe a mensagem
    - data_size: tamanho dos dados úteis a serem enviados
    - total_size: tamanho de todos os pacotes somados
    - bytes: lista de bytes dos dados separados em pacotes

    '''

    def __init__(self, data):
        '''
        Inicializa um objeto Message

        Parâmetros:
        - data: lista de bytes dos dados não separados
        
        '''

        # amarra o argumento à instância de Message
        self.data = data

        # extrai as especificações dos pacotes
        max_data = Packet.MAX_DATA
        max_payload = Packet.MAX_PAYLOAD

        # verifica a validade dos argumentos
        if len(data) > max_data: raise ValueError('Mensagem grande demais')

        # calcula a quantidade de datagramas necessários
        number_of_datagrams = math.ceil(len(data) / max_payload)

        # divide os dados brutos em pacotes  --- --- --- --- --- --- --- --- --- --- ---
        # e adiciona os bytes dos pacotes à lista de bytes
        self.packets = dict()
        self.bytes = list()

        for i in range(number_of_datagrams):

            # intervalo para extrai dos dados brutos
            from_index = i * max_payload
            to_index = (i + 1) * max_payload

            # extrai o intervalo e cria um datagrama com o payload
            payload = data[from_index:to_index]
            packet = Packet(self, number_of_datagrams, i + 1, payload)

            # adiciona o datagrama à lista de datagramas e preenche a lista de bytes
            self.packets[i + 1] = packet
            self.bytes += packet.bytes

        #-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        # define demais propriedades
        self.total_size = len(self.bytes)
        self.data_size = len(self.data)






