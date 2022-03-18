"""
Arquivo criado para armazenar a classe Packet

"""

import utils
import numpy as np


class Packet:
    '''
    Representa um tipo de pacote definido por um datagrama.

    Está sempre associado a um objeto Message, porque não existem
    pacotes avulsos, apenas mensagens de pacote único.

    Propriedades:
    - ammount: quantidade de pacotes 
    - message: objeto Message ao qual o pacote pertence
    - number: identidade do pacote
    - data_list: dados úteis do pacote (lista de bytes separados)
    - head_list: lista de bytes separados que compõem o HEAD
    - payload_list: lista de bytes do payload
    - bytes_list: lista de bytes do pacote completo
    - data_size: quantidade de dados úteis em bytes
    - sendable: pacote pronto para envio

    '''

    # especificações do datagrama para referenciamento  --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    HEAD_START_SIZE = 2                     # quantidade de bytes que compõem o início do HEAD
    NUMBER_SIZE = 2                         # tamanho do número do pacote em bytes
    SIZE_INDICATOR_SIZE = 1                 # tamanho do número que indica o tamanho do payload
    HEAD_END_SIZE = 3                       # quantidade de bytes que compõem o fim do HEAD
    PAYLOAD_SIZE = 114                      # tamanho do payload em bytes
    EOP_SIZE = 4                            # tamanho do EOP em bytes
    #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

    # especificações derivadas  --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    HEAD_SIZE =  HEAD_START_SIZE + NUMBER_SIZE * 2 + SIZE_INDICATOR_SIZE + HEAD_END_SIZE
    MAX_PACKETS = 256 ** NUMBER_SIZE                        # quantidade máxima de pacotes em uma mensagem
    MAX_DATA = MAX_PACKETS * PAYLOAD_SIZE                   # quantidade máxima de bytes úteis
    PACKET_SIZE = HEAD_SIZE + PAYLOAD_SIZE + EOP_SIZE       # tamanho de um único pacote
    #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

    # bytes de sinalização de início e fim do HEAD e EOP
    PAYLOAD_FILLER = [b'\x55']
    HEAD_START_LIST = [b'\xAA'] * HEAD_START_SIZE
    HEAD_END_LIST = [b'\xAA'] * HEAD_END_SIZE
    EOP_LIST = [b'\xBB'] * EOP_SIZE

    # HEAD genérico para comparação com HEADs de pacotes recebidos
    SAMPLE_HEAD = HEAD_START_LIST + ['ammount'] * NUMBER_SIZE + ['number'] * NUMBER_SIZE + ['size'] * SIZE_INDICATOR_SIZE + HEAD_END_LIST

    def __init__(self, message, number, data):
        '''
        Inicializa um único pacote pertencente a uma mensagem

        Parâmetros:
        - message: objeto Message ao qual o pacote pertence
        - number: número do pacote (int) (o número 1 é o primeiro)
        - data: dados (lista de bytes)

        '''

        # cria uma variável para o tamanho do payload e extrai o tamanho da mensagem em pacotes
        data_size = len(data)
        ammount = message.number_of_packets

        # verifica parâmetros inválidos
        if number > ammount: raise ValueError('Número do pacote maior que o número total de pacotes')
        if data_size > Packet.PAYLOAD_SIZE: raise ValueError('Payload grande demais')

        # amarra os argumentos ao objeto
        self.message = message
        self.ammount = ammount
        self.number = number
        self.data_list = data
        self.data_size = data_size

        # MONTAGEM DO HEAD  --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        # conversão de number e ammount para 3 bytes cada
        data_size_bytes = data_size.to_bytes(Packet.SIZE_INDICATOR_SIZE, byteorder="big")
        ammount_bytes = ammount.to_bytes(Packet.NUMBER_SIZE, byteorder="big")
        number_bytes = number.to_bytes(Packet.NUMBER_SIZE, byteorder="big")
        data_size_bytes_list = utils.splitBytes(data_size_bytes)
        ammount_bytes_list = utils.splitBytes(ammount_bytes)
        number_bytes_list = utils.splitBytes(number_bytes)

        # junção dos componentes do head
        self.head_list = Packet.HEAD_START_LIST + ammount_bytes_list + number_bytes_list + data_size_bytes_list + Packet.HEAD_END_LIST

        #   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

        # preenchimento do payload
        self.payload_list = self.data_list
        while len(self.payload_list) < Packet.PAYLOAD_SIZE:
            self.payload_list += Packet.PAYLOAD_FILLER

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










