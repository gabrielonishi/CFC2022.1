import numpy as np
import utils

class Packet:
    """
    Classe abstrata que representa um pacote

    Propriedades:
    - head: lista com o head
    - payload: lista com o payload
    - eop: lista com o eop
    - bytes_list: lista com toda a mensagem pronta
    - sendable: lista pronta pra ser enviada
    """

    MESSAGE_TYPE_SIZE = 1                   # h0: bytes reservados p/ informar tipo de mensagem
    FREE_BYTES_SIZE = 2                     # h1 e h2: quantidade de bytes livres, xAA
    SIZE_INDICATOR_SIZE = 1                 # h3: bytes reservados p/ informar o número total de pacotes
    NUMBER_SIZE = 1                         # h4: bytes reservados p/ informar o número do pacote
    ID_OR_PAYLOAD_SIZE = 1                  # h5: bytes reservados p/ id se for handshake e tamanho do payload se for dado
    EXPECTED_NUMBER_SIZE = 1                # h6: bytes reservados p/ informar quando há erro no envio
    LAST_RECEIVED_SIZE = 1                  # h7: bytes reservados p/ informar o número do último pacote recebido com sucesso
    CRC_SIZE = 2                            # h8 e h9: bytes reservados p/ informar o CRC. Por enquanto não usamos, xAA
    HEAD_SIZE = 10                          # tamanho do head
    MAX_PAYLOAD_SIZE = 114                  # tamanho máximo payload em bytes
    EOP_SIZE = 4                            # tamanho do EOP em bytes
    FILLER = [b'\xAA']

    def __init__(self, head:list, payload:list):
        self.head = head
        self.payload = payload
        self.eop = [b'\xAA', b'\xBB', b'\xCC', b'\xDD']
        self.bytes_list = self.head + self.payload + self.eop
        self.sendable = np.asarray(self.bytes_list)    


class Type1(Packet):
    """
    Classe para padronizar mensagens do tipo 1
    
    Representa um chamado do cliente enviando ao servidor convidando-o 
    à transmissão

    Propriedades:
    - message_type: tipo de mensagem 
    - server_id: número do servidor destinatário
    - ammount: quantidade total de pacotes a serem enviados
    - number: número do pacote que envia (por padrão, handshake é 0)
    - size: tamanho da mensagem

    """
    
    SIZE = Packet.HEAD_SIZE + Packet.EOP_SIZE

    def __init__(self, server_id:int, ammount:int):

        # Verificando erros:
        if ammount>256: raise ValueError("Mensagem grande demais!")
        
        self.message_type = 1
        self.server_id = server_id
        self.ammount = ammount
        self.id = server_id
        self.number = 0
        
        h0 = [self.message_type.to_bytes(1, byteorder="big")]
        h1 = Packet.FILLER
        h2 = Packet.FILLER
        h3 = [self.ammount.to_bytes(1, byteorder="big")]
        h4 = [self.number.to_bytes(1, byteorder="big")]
        h5 = [self.server_id.to_bytes(1,byteorder="big")]
        h6 = Packet.FILLER
        h7 = Packet.FILLER
        h8 = Packet.FILLER
        h9 = Packet.FILLER
        
        head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
        payload = []

        self.size = Packet.HEAD_SIZE + Packet.EOP_SIZE

        super().__init__(head=head, payload=payload)

class Type2(Packet):
    """
    Classe para padronizar mensagens do tipo 2

    Enviada pelo servidor ao cliente, após o primeiro receber uma 
    mensagem tipo 1 com o número identificador correto

    Propriedades:
    - message_type: tipo de mensagem 
    - id: id do receptor do pacote

    """

    SIZE = Packet.HEAD_SIZE + Packet.EOP_SIZE

    def __init__(self, client_id:int):

        self.message_type = 2
        self.client_id = client_id
        
        h0 = [self.message_type.to_bytes(1, byteorder="big")]
        h1 = Packet.FILLER
        h2 = Packet.FILLER
        h3 = Packet.FILLER
        h4 = Packet.FILLER
        h5 = [self.client_id.to_bytes(1, byteorder="big")]
        h6 = Packet.FILLER
        h7 = Packet.FILLER
        h8 = Packet.FILLER
        h9 = Packet.FILLER
        
        head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
        payload = []

        super().__init__(head=head, payload=payload)
    
class Type3(Packet):
    """
    Classe para padronizar mensagens do tipo 3

    Mensagem de dados. Contém de fato um bloco do dado a ser 
    enviado (payload).

    Propriedades:
    - message_type: tipo de mensagem
    - ammount: quantidade total de pacotes a serem enviados
    - number: número do pacote que envia (começa do 1)
    - data: lista de bytes de dados(irão no payload)

    """

    def __init__(self, ammount:int, number:int, data:list):

        # Verificando erros:
        if len(data)>Packet.MAX_PAYLOAD_SIZE: raise ValueError("Payload grande demais!")
        if ammount>256: raise ValueError("Mensagem grande demais!")

        self.message_type = 3
        self.ammount = ammount
        self.number = number
        self.data = data
        self.payload_size = len(data)
        
        h0 = [self.message_type.to_bytes(1, byteorder="big")]
        h1 = Packet.FILLER
        h2 = Packet.FILLER
        h3 = [self.ammount.to_bytes(1, byteorder="big")]
        h4 = [self.number.to_bytes(1, byteorder="big")]
        h5 = [self.payload_size.to_bytes(1, byteorder="big")]
        h6 = Packet.FILLER
        h7 = Packet.FILLER
        h8 = Packet.FILLER
        h9 = Packet.FILLER
        
        head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
        payload = data

        self.size = Packet.HEAD_SIZE + len(payload) + Packet.EOP_SIZE

        super().__init__(head=head, payload=payload)

class Type4(Packet):
    """
    Classe para padronizar mensagens do tipo 4

    Enviada do servidor para o cliente toda vez que uma mensagem 
    tipo 3 é recebida pelo servidor e averiguada  

    Propriedades:
    - message_type: tipo de mensagem
    - last_received: número do último pacote a ser recebido

    """
    
    SIZE = Packet.HEAD_SIZE + Packet.EOP_SIZE

    def __init__(self, last_received: int):

        self.message_type = 4
        self.last_received = last_received
        
        h0 = [self.message_type.to_bytes(1, byteorder="big")]
        h1 = Packet.FILLER
        h2 = Packet.FILLER
        h3 = Packet.FILLER
        h4 = Packet.FILLER
        h5 = Packet.FILLER
        h6 = Packet.FILLER
        h7 = [self.last_received.to_bytes(1, byteorder="big")]
        h8 = Packet.FILLER
        h9 = Packet.FILLER
        
        head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
        payload = []

        super().__init__(head=head, payload=payload)
    
class Type5(Packet):
    """
    Classe para padronizar mensagens do tipo 5

    Mensagem de timeout. Toda vez que o limite de espera exceder
    o timer dedicado a isso, em qualquer um dos lados, deve-se
    enviar essa mensagem e finalizar a conexão

    Propriedades:
    - message_type: tipo de mensagem

    """
    SIZE = Packet.HEAD_SIZE + Packet.EOP_SIZE

    def __init__(self):

        self.message_type = 5
        
        h0 = [self.message_type.to_bytes(1, byteorder="big")]
        h1 = Packet.FILLER
        h2 = Packet.FILLER
        h3 = Packet.FILLER
        h4 = Packet.FILLER
        h5 = Packet.FILLER
        h6 = Packet.FILLER
        h7 = Packet.FILLER
        h8 = Packet.FILLER
        h9 = Packet.FILLER
        
        head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
        payload = []

        super().__init__(head=head, payload=payload)

class Type6(Packet):
    """
    Classe para padronizar mensagens do tipo 6

    Mensagem de erro. O servidor deve enviar esta mensagem ao cliente 
    toda vez que receber uma mensagem tipo 3 inválida, seja por 
    estar com bytes faltando, fora do formato correto ou por não 
    ser o pacote esperado pelo servidor (pacote repetido ou fora da 
    ordem)

    Propriedades:
    - message_type: tipo de mensagem
    - expected_number: número correto do pacote esperado

    """

    SIZE = Packet.HEAD_SIZE + Packet.EOP_SIZE

    def __init__(self, expected_number:int):

        self.message_type = 6
        self.expected_number = expected_number
        
        h0 = [self.message_type.to_bytes(1, byteorder="big")]
        h1 = Packet.FILLER
        h2 = Packet.FILLER
        h3 = Packet.FILLER
        h4 = Packet.FILLER
        h5 = Packet.FILLER
        h6 = [self.expected_number.to_bytes(1, byteorder="big")]
        h7 = Packet.FILLER
        h8 = Packet.FILLER
        h9 = Packet.FILLER
        
        head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
        payload = []

        super().__init__(head=head, payload=payload)