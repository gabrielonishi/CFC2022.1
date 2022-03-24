

import math
import numpy as np

import utils
from packet import Packet

class Message:
    '''
    Classe abstrata que representa uma mensagem a ser enviada.
    É herdada por MessageIn e MessageOut.
    É essencialmente uma conjunto de Packets

    '''

    def __init__(self):
        ''' Inicializa um objeto Message '''

        # propriedades:
        self.type = int()               # tipo da mensagem (1, 2, 3, 4, 5 ou 6)
        self.data = list()              # lista de bytes individuais dos dados úteis a serem enviados
        self.packets = dict()           # dicionário de pacotes (id -> pacote)
        self.data_size = int()          # quantidade de bytes que compõem os dados úteis
        self.number_of_packets = int()  # número total de pacotes que compõem a mensagem


    def __eq__(self, other):
        ''' Overload do comparador de igualdade '''

        # verifica se other é Message também
        if not isinstance(other, Message): return False

        # verifica o tamanho de ambas as instâncias
        if self.data_size != other.data_size: return False

        # percorre todos os pacotes de ambas as instâncias
        equal = True
        for i in range(1, self.number_of_packets + 1):
            equal = equal and (self.packets[i] == other.packets[i])
            if not equal: return False

        return True



