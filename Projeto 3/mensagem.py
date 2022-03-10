'''
Arquivo criado para armazenar a classe de Datagrama

'''

import utils

from datagrama import Datagram

class Message():
    ''' Classe que representa uma mensagem a ser enviada dividida em datagramas '''

    def __init__(self, raw_data):
        '''
        Inicializa um objeto Message

        Parâmetros:
        - raw_data: lista de bytes a serem enviados
        
        '''

        # verifica a validade dos argumentos
        if len(raw_data) > 256 ** 3 * 114: raise ValueError('Mensagem grande demais')

        # divide os dados brutos em uma lista de payloads
        self.size_datagrams = round(len(raw_data) / 114)
        if len(raw_data) % 114 > 0: self.size_datagrams += 1

        # mensagem dividida em datagramas
        self.datagrams = list()

        for i in range(self.size_datagrams):
            payload = 
            datagram = Datagram(i + 1, self.size_datagrams, )

