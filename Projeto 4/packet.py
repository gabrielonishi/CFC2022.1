"""
Arquivo criado para armazenar a classe Packet

"""

import utils
import numpy as np
from protocol import Protocol

class Packet:
    '''
    Representa um tipo de pacote definido por um datagrama.

    Está sempre associado a um objeto Message, porque não existem
    pacotes avulsos, apenas mensagens de pacote único.

    Propriedades:
    - ammount: quantidade de pacotes 
    - message: objeto Message ao qual o pacote pertence
    - message_type: tipo de mensagem (varia de 1-6)
    - number: identidade do pacote
    - data_list: dados úteis do pacote (lista de bytes separados)
    - head_list: lista de bytes separados que compõem o HEAD
    - payload_list: lista de bytes do payload
    - bytes_list: lista de bytes do pacote completo
    - data_size: quantidade de dados úteis em bytes
    - sendable: pacote pronto para envio

    '''

    # define os templates
    HEAD_TEMPLATES = {
        1: [b'\x01', b'\xAA', b'\xAA', b'\x01', b'\x01', 'server_id', b'\x00', b'\x00', b'\xAA', b'\xAA'],
        2: [b'\x02', b'\xAA', b'\xAA', b'\x01', b'\x01', 'client_id', b'\x00', b'\x00', b'\xAA', b'\xAA'],
        3: [b'\x03', b'\xAA', b'\xAA', 'number_of_packets', 'packet_id', 'payload_size', b'\x00', b'\x00', b'\xAA', b'\xAA'],
        4: [b'\x04', b'\xAA', b'\xAA', b'\x01', b'\x01', b'\x00', b'\x00', 'last_successful_packet', b'\xAA', b'\xAA'],
        5: [b'\x05', b'\xAA', b'\xAA', b'\x01', b'\x01', b'\x00', b'\x00', b'\x00', b'\xAA', b'\xAA'],
        6: [b'\x06', b'\xAA', b'\xAA', b'\x01', b'\x01', b'\x00', 'wanted_packet', b'\x00', b'\xAA', b'\xAA']
    }

    # especificações do datagrama para referenciamento  --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    MESSAGE_TYPE_SIZE = 1                   # h0: bytes reservados p/ informar tipo de mensagem
    
    # ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
    # Ver o que fazer com esses bytes livres
    FREE_BYTES_SIZE = 2                     # h1 e h2: quantidade de bytes livres, xAA
    # ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
    
    SIZE_INDICATOR_SIZE = 1                 # h3: bytes reservados p/ informar o número total de pacotes
    NUMBER_SIZE = 1                         # h4: bytes reservados p/ informar o número do pacote
    ID_OR_PAYLOAD_SIZE                      # h5: bytes reservados p/ id se for handshake e tamanho do payload se for dado
    ERROR_SIZE                              # h6: bytes reservados p/ informar quando há erro no envio
    LAST_GOOD_PACKET_SIZE                   # h7: bytes reservados p/ informar o número do último pacote recebido com sucesso
    CRC_SIZE = 3                            # h8 e h9: bytes reservados p/ informar o CRC. Por enquanto não usamos, xAA
    MAX_PAYLOAD_SIZE = 114                  # tamanho do payload em bytes
    EOP_SIZE = 4                            # tamanho do EOP em bytes
    #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

    # especificações derivadas  --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    HEAD_SIZE = (MESSAGE_TYPE_SIZE + HEAD_START_SIZE + AMMOUNT_SIZE 
    + NUMBER_SIZE + ID_OR_PAYLOAD_SIZE + ERROR_SIZE + LAST_GOOD_PACKET_SIZE 
    + CRC_SIZE + MAX_PAYLOAD_SIZE + EOP_SIZE)               # tamanho do head
    MAX_PACKETS = 256 ** NUMBER_SIZE                        # quantidade máxima de pacotes em uma mensagem
    MAX_DATA = MAX_PACKETS * MAX_PAYLOAD_SIZE               # quantidade máxima de bytes úteis
    #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

    # bytes de sinalização de início e fim do HEAD e EOP
    FREE_BYTES_LIST = [b'\xAA'] * FREE_BYTES_SIZE
    CRC_LIST = [b'\xAA'] * 2
    EOP_LIST = [b'\xAA' + b'\xBB' + b'\xCC' + b'\xDD']      # padronizado pelo enunciado do projeto

    # gerando um template pra sabermos como vai ser o formato do head
    HEAD_TEMPLATE = (['tipo'] + FREE_BYTES_LIST + ['size'] + ['number']
    + ['number'] + ['id ou payload'] + ['error'] + ['último pacote recebido'] + CRC_LIST)

    def __init__(self, message, head_info, data):
        '''
        Inicializa um único pacote pertencente a uma mensagem

        Parâmetros:
        - message: objeto Message ao qual o pacote pertence
        - head_info: número do pacote (int) (o número 1 é o primeiro)
        - data: dados (lista de bytes)

        '''

        head_info['number_of_payload'] = len(data)

        # cria uma variável para o tamanho do payload e extrai o tamanho da mensagem em pacotes
        data_size = len(data)
        ammount = message.number_of_packets

        # amarra os argumentos ao objeto
        self.message = message
        self.message_type = message.type
        self.ammount = ammount
        self.number = number
        self.data_list = data
        self.data_size = data_size

        # MONTAGEM DO HEAD  --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        # conversão de number e ammount para 1 byte cada
        data_size_bytes = data_size.to_bytes(Packet.SIZE_INDICATOR_SIZE, byteorder="big")
        ammount_bytes = ammount.to_bytes(Packet.NUMBER_SIZE, byteorder="big")
        number_bytes = number.to_bytes(Packet.NUMBER_SIZE, byteorder="big")
        message_type_bytes = message.type.to_bytes(Packet.MESSAGE_TYPE_SIZE, byteorder="big")
        data_size_bytes_list = utils.splitBytes(data_size_bytes)
        ammount_bytes_list = utils.splitBytes(ammount_bytes)
        number_bytes_list = utils.splitBytes(number_bytes)

    #     HEAD_TEMPLATES = {
    #     1: [b'\x01', b'\xAA', b'\xAA', b'\x01', b'\x01', 'server_id', b'\x00', b'\x00', b'\xAA', b'\xAA'],
    #     2: [b'\x02', b'\xAA', b'\xAA', b'\x01', b'\x01', 'client_id', b'\x00', b'\x00', b'\xAA', b'\xAA'],
    #     3: [b'\x03', b'\xAA', b'\xAA', 'number_of_packets', 'packet_id', 'payload_size', b'\x00', b'\x00', b'\xAA', b'\xAA'],
    #     4: [b'\x04', b'\xAA', b'\xAA', b'\x01', b'\x01', b'\x00', b'\x00', 'last_successful_packet', b'\xAA', b'\xAA'],
    #     5: [b'\x05', b'\xAA', b'\xAA', b'\x01', b'\x01', b'\x00', b'\x00', b'\x00', b'\xAA', b'\xAA'],
    #     6: [b'\x06', b'\xAA', b'\xAA', b'\x01', b'\x01', b'\x00', 'wanted_packet', b'\x00', b'\xAA', b'\xAA']
    # }

        header = HEAD_TEMPLATES.get[message.type]
        for i in range(len(header)):
            if isinstance(header[i], str):
                if i == 3: header[3] = ammount_bytes
                if i == 4: header[4] = 


        #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        # junção das listas de bytes que formam o HEAD e o pacote completo
        self.bytes_list = self.head_list + self.payload_list + Packet.EOP_LIST
        self.sendable = np.asarray(self.bytes_list)

    

    @staticmethod
    def decode(message, raw_packet):
        '''
        Retorna um objeto Datagram a partir de uma lista de bytes de um datagrama recebido
        Retorna False se receber um pacote com especificações inesperadas
        
        Deve ser chamada somente pelo método receive_packet da classe Message

        Parâmetros:
        - message: instância de Message à qual o datagrama será atribuido
        - raw_datagram: dados brutos que seguem o formato do datagrama

        '''

        # extrai o HEAD e o EOP
        raw_packet = utils.splitBytes(raw_packet)
        head = raw_packet[ : Packet.HEAD_SIZE]
        eop = raw_packet[-1 * Packet.EOP_SIZE : ]

        # verifica a validade do HEAD e extrai os dados do HEAD --- --- --- --- --- ---
        for i in range(Packet.HEAD_SIZE):

            expected_value = Packet.SAMPLE_HEAD[i]
            received_byte = head[i]

            # lida com bytes variáveis
            if isinstance(expected_value, str):
                if expected_value == 'ammount': ammount = int.from_bytes(received_byte, 'big'); continue
                if expected_value == 'number': number = int.from_bytes(received_byte, 'big'); continue
                if expected_value == 'size': data_size = int.from_bytes(received_byte, 'big'); continue

            # lida com bytes fixos
            else:
                if received_byte != expected_value: return None
        #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        # verifica a validade do EOP
        if eop != Packet.EOP_LIST:
            print("EOP invalid")
            return None

        # extrai o payload
        payload = raw_packet[Packet.HEAD_SIZE : -1 * Packet.EOP_SIZE]
        data = payload[ : data_size]

        # cria a nova instância de Datagrama
        message.number_of_packets = ammount
        packet = Packet(message, number, data)

        return packet


    def __eq__(self, other):
        ''' Overload do comparador de igualdade '''

        # verifica se other é Packet
        if not isinstance(other, Packet): return False

        # renomeia propriedades
        size = self.data_size

        # verifica o tamanho de ambas as instâncias
        if self.data_size != other.data_size: return False

        # percorre todos os bytes dos dados de ambos as instâncias
        equal = True
        for i in range(size):
            equal = equal and (self.data_list[i] == other.data_list[i])
            if not equal: return False

        return True










