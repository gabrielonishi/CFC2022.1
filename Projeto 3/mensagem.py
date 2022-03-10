'''
Arquivo criado para armazenar a classe de Datagrama

'''

import math
import utils

from datagrama import Datagram

class Message():
    '''

    Classe que representa uma mensagem a ser enviada dividida em datagramas

    Propriedades:
    - datagrams: lista de Datagrams que compõe a mensagem
    - bytes: lista de bytes que compõem a mensagem finalizada (é o que é transmitido)

    '''

    def __init__(self, raw_data):
        '''
        Inicializa um objeto Message

        Parâmetros:
        - raw_data: lista de bytes a serem enviados
        
        '''

        # extrai as especificações do datagrama
        max_ammount = Datagram.MAX_AMMOUNT
        max_payload = Datagram.MAX_PAYLOAD

        # verifica a validade dos argumentos
        if len(raw_data) > max_ammount * max_payload: raise ValueError('Mensagem grande demais')

        # calcula a quantidade de datagramas necessários
        number_of_datagrams = math.ceil(len(raw_data) / max_payload)

        # divide os dados brutos em datagramas  --- --- --- --- --- --- --- --- --- --- ---
        # e cria a lista de bytes da mensagem
        self.datagrams = list()
        self.bytes = list()

        for i in range(number_of_datagrams):

            # intervalo para extrai dos dados brutos
            from_index = i * max_payload
            to_index = (i + 1) * max_payload

            # extrai o intervalo e cria um datagrama com o payload
            payload = raw_data[from_index:to_index]
            datagram = Datagram(number_of_datagrams, i + 1, payload)

            # adiciona o datagrama à lista de datagramas e preenche a lista de bytes
            self.datagrams.append(datagram)
            self.bytes += datagram.bytes

        #-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---










