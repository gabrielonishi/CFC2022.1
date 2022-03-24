from message import Message
from packet import Packet

import numpy as np


class MessageIn(Message):
    ''' Classe que representa uma mensagem a ser recebida '''

    def __init__(self):
        ''' Instancializa uma mensagem a ser recebida '''
        
        # inicializa a class Message
        super().__init__()

        # propriedades próprias
        self.is_complete = False
        self.last_received = 0

    
    def receiveHandshake(self, handshake_message):
        ''' Avalia um handshake para definir dados da mensagem '''
        pass

    
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
        self.data_list += received_packet.data_list

        # atualiza demais propriedades
        self.number_of_packets = received_packet.ammount
        self.total_size += Packet.PACKET_SIZE
        self.data_size += received_packet.data_size
        self.bytes = np.asarray(self.data_list)
        
        return True

