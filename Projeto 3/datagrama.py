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
    
    '''

    # bytes de sinalização de início e fim do HEAD e EOP
    HEAD_TIPS_BYTES = [b'\xAA'] * 2
    EOP_BYTES = [b'\xBB'] * 4

    # especificações do datagrama para referenciamento externo
    MAX_PAYLOAD = 114       # tamanho do payload em bytes
    MAX_AMMOUNT = 256 ** 3  # quantidade máxima de datagramas em uma mensagem

    def __init__(self, ammount, number, payload):
        '''
        Inicializa um único datagrama pertencente a um grupo de datagramas (pacote)

        Parâmetros:
        - ammount: número total de datagramas (int)
        - number: número do datagrama (int) (o número 1 é o primeiro)
        - payload: dados (lista de bytes, no máximo 114 bytes)

        '''

        # verifica parâmetros inválidos
        if ammount > Datagram.MAX_AMMOUNT: raise ValueError('Impossível enviar tantos pacotes')
        if number > ammount: raise ValueError('Número do pacote maior que o número total de pacotes')
        if len(payload) > Datagram.MAX_PAYLOAD: raise ValueError('Payload grande demais')

        # amarra os argumentos ao objeto
        self.ammount = ammount
        self.number = number
        self.payload = payload

        # conversão de number e ammount para 3 bytes cada
        ammount_bytes = ammount.to_bytes(3, byteorder="big")
        number_bytes = number.to_bytes(3, byteorder="big")

        # separação dos bytes
        ammount_bytes = utils.split_bytes(ammount_bytes)
        number_bytes = utils.split_bytes(number_bytes)

        # junção das listas de bytes que formam o HEAD e o datagrama completo
        self.head = Datagram.HEAD_TIPS_BYTES + ammount_bytes + number_bytes + Datagram.HEAD_TIPS_BYTES
        self.bytes = self.head + self.payload + Datagram.EOP_BYTES
        


