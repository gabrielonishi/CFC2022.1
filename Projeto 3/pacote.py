"""
Arquivo criado para armazenar a classe Packet

"""

import utils

class Packet():
    '''
    Representa um tipo de pacote definido pelo datagrama especificado no enunciado

    10 bytes - HEAD: AA AA {qtde total de datagramas} {número do datagrama} AA AA
    1 a 114 bytes - PAYLOAD
    4 bytes - EOP: BB BB BB BB

    Propriedades:
    - ammount: quantidade de datagramas 
    - message: objeto Message ao qual o pacote pertence
    - ammount: quantidade de pacotes
    - number: identidade do pacote
    - payload: dados do pacote
    - head: lista de bytes que compõem o HEAD
    - bytes: lista de bytes pronta para envio
    - data_size: tamanho do payload em bytes
    - total_size: tamanho do pacote em bytes

    '''

    # especificações do datagrama para referenciamento
    HEAD_SIZE = 10                          # tamanho do HEAD em bytes
    MAX_PAYLOAD = 114                       # tamanho do payload em bytes
    EOP_SIZE = 4                            # tamanho do EOP em bytes
    NUMBER_SIZE = 3                         # tamanho do número do datagrama em bytes
    MAX_AMMOUNT = 256 ** NUMBER_SIZE        # quantidade máxima de datagramas em uma mensagem
    MAX_DATA = MAX_AMMOUNT * MAX_PAYLOAD    # quantidade máxima de bytes úteis
    HEAD_TIPS_SIZE = ((HEAD_SIZE - NUMBER_SIZE * 2) / 2)    # tamanho das "bandeiras" do HEAD
    MAX_SIZE = HEAD_SIZE + MAX_PAYLOAD + EOP_SIZE           # tamanho máximo do datagrama inteiro

    # verifica a validade das especificações
    if int(HEAD_TIPS_SIZE) != HEAD_TIPS_SIZE:
        raise ValueError('Especificações do datagrama inválidas')
    HEAD_TIPS_SIZE = int(HEAD_TIPS_SIZE)

    # bytes de sinalização de início e fim do HEAD e EOP
    HEAD_TIPS_BYTES = [b'\xAA'] * int((HEAD_SIZE - NUMBER_SIZE * 2) / 2)
    EOP_BYTES = [b'\xBB'] * EOP_SIZE

    def __init__(self, message, ammount, number, payload):
        '''
        Inicializa um único pacote pertencente a uma mensagem

        Parâmetros:
        - message: objeto Message para agrupar datagramas relacionados
        - ammount: número total de datagramas (int)
        - number: número do datagrama (int) (o número 1 é o primeiro)
        - payload: dados (lista de bytes, no máximo 114 bytes)

        '''

        # verifica parâmetros inválidos
        if ammount > Packet.MAX_AMMOUNT: raise ValueError('Impossível enviar tantos pacotes')
        if number > ammount: raise ValueError('Número do pacote maior que o número total de pacotes')
        if len(payload) > Packet.MAX_PAYLOAD: raise ValueError('Payload grande demais')

        # amarra os argumentos ao objeto
        self.message = message
        self.ammount = ammount
        self.number = number
        self.payload = payload

        # conversão de number e ammount para 3 bytes cada
        ammount_bytes = ammount.to_bytes(Packet.NUMBER_SIZE, byteorder="big")
        number_bytes = number.to_bytes(Packet.NUMBER_SIZE, byteorder="big")
        ammount_bytes = utils.split_bytes(ammount_bytes)
        number_bytes = utils.split_bytes(number_bytes)

        # junção das listas de bytes que formam o HEAD e o pacote completo
        self.head = Packet.HEAD_TIPS_BYTES + ammount_bytes + number_bytes + Packet.HEAD_TIPS_BYTES
        self.bytes = self.head + self.payload + Packet.EOP_BYTES

        # definição de demais propriedades
        self.data_size = len(self.payload)
        self.total_size = len(self.bytes)
    

        







