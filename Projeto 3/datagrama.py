"""
Arquivo criado para armazenar a classe de Datagrama

"""

import utils

class Datagram():
    '''
    Representa um datagrama do tipo especificado no enunciado

    10 bytes - HEAD: AA AA {qtde total de datagramas} {número do datagrama} AA AA
    1 a 114 bytes - PAYLOAD
    4 bytes - EOP: BB BB BB BB

    Propriedades:
    - ammount: quantidade de datagramas 

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
        Inicializa um único datagrama pertencente a um grupo de datagramas (pacote)

        Parâmetros:
        - message: objeto Message para agrupar datagramas relacionados
        - ammount: número total de datagramas (int)
        - number: número do datagrama (int) (o número 1 é o primeiro)
        - payload: dados (lista de bytes, no máximo 114 bytes)

        '''

        # verifica parâmetros inválidos
        if ammount > Datagram.MAX_AMMOUNT: raise ValueError('Impossível enviar tantos pacotes')
        if number > ammount: raise ValueError('Número do pacote maior que o número total de pacotes')
        if len(payload) > Datagram.MAX_PAYLOAD: raise ValueError('Payload grande demais')

        # amarra os argumentos ao objeto
        self.message = message
        self.ammount = ammount
        self.number = number
        self.payload = payload

        # conversão de number e ammount para 3 bytes cada
        ammount_bytes = ammount.to_bytes(Datagram.NUMBER_SIZE, byteorder="big")
        number_bytes = number.to_bytes(Datagram.NUMBER_SIZE, byteorder="big")
        ammount_bytes = utils.split_bytes(ammount_bytes)
        number_bytes = utils.split_bytes(number_bytes)

        # junção das listas de bytes que formam o HEAD e o datagrama completo
        self.head = Datagram.HEAD_TIPS_BYTES + ammount_bytes + number_bytes + Datagram.HEAD_TIPS_BYTES
        self.bytes = self.head + self.payload + Datagram.EOP_BYTES
    

    @staticmethod
    def decode(message, raw_datagram):
        '''
        Retorna um objeto Datagram a partir de uma lista de bytes de um datagrama recebido
        Deve ser chamada somente pelo método estático decode da classe Message

        Parâmetros:
        - message: instância de Message à qual o datagrama será atribuido
        - raw_datagram: dados brutos que seguem o formato do datagrama

        '''

        # extrai o HEAD e o EOP
        head = raw_datagram[ : Datagram.HEAD_SIZE]
        eop = raw_datagram[-1 * Datagram.EOP_SIZE : ]

        # verifica a validade do HEAD
        for i in range(Datagram.HEAD_TIPS_SIZE):
            inverted_i = (-1 * i) - 1
            invalid = head[inverted_i] != Datagram.HEAD_TIPS_BYTES[inverted_i]
            invalid = invalid or head[i] != Datagram.HEAD_TIPS_BYTES[i]
            if invalid: raise ValueError('HEAD inválido')

        # verifica a validade do EOP
        if eop != Datagram.EOP_BYTES: raise ValueError('EOP inválido')

        # extrai a parte útil do HEAD
        head_info = head[Datagram.HEAD_TIPS_SIZE : -1 * Datagram.HEAD_TIPS_SIZE]

        # extrai a quantidade de datagramas e o número do datagrama
        ammount = b''.join(head_info[:3])
        number = b''.join(head_info[3:])
        ammount = int.from_bytes(ammount, "big")
        number = int.from_bytes(number, "big")

        # extrai o payload
        payload = raw_datagram[Datagram.HEAD_SIZE : -1 * Datagram.EOP_SIZE]
        
        # cria a nova instância de Datagrama
        datagrama = Datagram(message, ammount, number, payload)

        return datagrama

        







