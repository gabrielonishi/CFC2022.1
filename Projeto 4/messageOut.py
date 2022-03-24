
from message import Message
from packet import Packet

import math

class MessageOut(Message):
    ''' Classe que representa uma mensagem a ser enviada '''
    
    
    def __init__(self, message_type, data):
        '''
        Cria uma nova instância de MessageOut

        Parâmetros:
        - message_type: tipo da mensagem (1, 2, 3, 4, 5 ou 6)
        - data: lista de bytes individuais a serem enviados
        
        '''

        # verifica a validade dos argumentos    --- --- --- --- --- --- --- --- --- --- ---
        if not isinstance(message_type, int):
            raise TypeError('O parâmetro "message_type" tem que ser um inteiro')
        if message_type < 1 or message_type > 6:
            raise ValueError('O valor de "message_type" tem que ser de 1 a 6')
        if not isinstance(data, list):
            raise TypeError('O parâmetro "data" tem que ser uma lista de bytes individuais')
        #-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        # inicializa a class Message
        super().__init__()

        # inicializa algumas propriedades de Message
        self.data = data
        self.type = message_type
        self.data_size = len(self.data)

        # calcula a quantidade de pacotes necessários
        self.number_of_packets = math.ceil(self.data_size / Packet.MAX_PAYLOAD_SIZE)

        # loop de fragmentação
        for packet_id in range(self.number_of_packets):

            # intervalo para extrair dos dados brutos
            from_index = packet_id * Packet.MAX_PAYLOAD_SIZE
            to_index = (packet_id + 1) * Packet.MAX_PAYLOAD_SIZE

            # extrai o intervalo e cria um Packet com os dados
            packet_data = self.data_list[from_index:to_index]
            packet = Packet(self, packet_id + 1, packet_data)

            # adiciona o pacote ao dicionário de pacotes
            self.packets[packet_id + 1] = packet

        #-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---



