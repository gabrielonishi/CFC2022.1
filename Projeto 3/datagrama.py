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

    def __init__(self, number, ammount, payload):
        '''
        Inicializa um único datagrama pertencente a um grupo de datagramas (pacote)

        Parâmetros:
        - number: número do datagrama (int) (o número 1 é o primeiro)
        - ammount: número total de datagramas (int)
        - payload: dados (lista de bytes, no máximo 114 bytes)

        '''

        # verifica parâmetros inválidos
        if ammount > 256 ** 3: raise ValueError('Impossível enviar tantos pacotes')
        if number > ammount: raise ValueError('Número do pacote maior que o número total de pacotes')
        if len(payload) > 114: raise ValueError('Payload grande demais')

        # amarra os argumentos ao objeto
        self.number = number
        self.ammount = ammount
        self.payload = payload

        # conversão de number e ammount para 3 bytes cada
        number_bytes = number.to_bytes(3, byteorder="big")
        ammount_bytes = ammount.to_bytes(3, byteorder="big")

        # separação dos bytes
        number_bytes = utils.split_bytes(number_bytes)
        ammount_bytes = utils.split_bytes(ammount_bytes)

        # junção das listas de bytes que formam o HEAD e o datagrama completo
        self.head = Datagram.HEAD_ENDS + ammount_bytes + number_bytes + Datagram.HEAD_ENDS
        self.bytes = self.head + self.payload + Datagram.EOP_BYTES
        


