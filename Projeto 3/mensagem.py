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
    - number_of_packets: quantidade de pacotes que compõem a mensagem
    - is_complete: se a mensagem está completa ou não

    '''

    def __init__(self, data=[]):
        '''
        Inicializa um objeto Message

        Parâmetros:
        - data: lista de bytes dos dados não separados
        
        '''

        # amarra o argumento à instância de Message
        self.data = data

        # determina se a mensagem está completa ou não
        if len(data) == 0:
            self.last_received = 0
            self.is_complete = False
        else:
            self.last_received = False
            self.is_complete = True

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
        self.bytes = list()

        for i in range(number_of_packets):

            # intervalo para extrair dos dados brutos
            from_index = i * payload_size
            to_index = (i + 1) * payload_size

            # extrai o intervalo e cria um datagrama com o payload
            payload = data[from_index:to_index]
            packet = Packet(self, i + 1, payload)

            # adiciona o datagrama à lista de datagramas e preenche a lista de bytes
            self.packets[i + 1] = packet
            self.bytes += packet.bytes

        #-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        # define demais propriedades
        self.total_size = len(self.bytes)
        self.data_size = len(self.data)


    def receive_packet(self, raw_packet):
        '''
        Adiciona um pacote recebido à mensagem
        Retorna False se o pacote recebido for inválido

        Parâmetros:
        - raw_packet: lista de bytes do pacote recebido
        
        '''

        if self.is_complete: raise TypeError('Essa mensagem já está completa')

        # decodifica o pacote e retorna False se houver falhas
        received_packet = Packet.decode(self, raw_packet)
        if received_packet == False: return False

        # verifica se o recebido é o próximo do último recebido
        if received_packet.number != self.last_received + 1: return False

        # verifica se a mensagem foi completada
        if self.last_received == self.number_of_packets: self.is_complete = True

        # adiciona os dados do pacote aos dados totais da mensagem
        self.packets[received_packet.number] = received_packet
        self.bytes += received_packet.bytes
        self.data += received_packet.data
        
        return received_packet


d_out = [b'\xFF'] * 2 ** 10
m_out = Message(d_out)

m_in = Message()

for i in range(1, m_out.number_of_packets + 1):
    packet = m_out.packets[i].bytes
    m_in.receive_packet(packet)

print(m_in.data == m_out.data)