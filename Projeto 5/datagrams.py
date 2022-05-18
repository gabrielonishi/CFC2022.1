import numpy as np
import utils
from crccheck.crc import Crc16

class Packet:
    """
    Classe abstrata que representa um pacote

    Propriedades:
    - head: lista com o head
    - payload: lista com o payload
    - eop: lista com o eop
    - bytes_list: lista com toda a mensagem pronta
    - bytes_raw: lsita com toda a mensagem junta
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
    FILLER = [b'\xAA']                      # byte de filler

    def __init__(self, head:list, payload:list):
        self.head = head
        self.payload = payload
        self.eop = [b'\xAA', b'\xBB', b'\xCC', b'\xDD']
        self.bytes_list = self.head + self.payload + self.eop
        self.bytes_raw = b"".join(self.bytes_list)
        self.sendable = np.asarray(self.bytes_list)
        self.size = Packet.HEAD_SIZE + len(payload) + Packet.EOP_SIZE 
        self.message_type = head[0]
        self.crc = utils.splitBytes(Crc16.calc(self.bytes_raw).to_bytes(Packet.CRC_SIZE, byteorder="big"))
        self.head = head[:-Packet.CRC_SIZE] + self.crc
        self.bytes_list = self.head + self.payload + self.eop
        self.bytes_raw = b"".join(self.bytes_list)
        self.sendable = np.asarray(self.bytes_list)
    
    def setCRC(self, new_crc):
        """
            Função introduzida apenas para testar o que aconteceria se o CRC 
            não for o esperado
        """
        self.crc = new_crc

    @staticmethod
    def decode(raw_packet):
        '''
        Retorna um objeto Packet a partir de uma lista de bytes de um datagrama recebido
        '''

        # extrai o HEAD e o EOP
        bytes_list = utils.splitBytes(raw_packet)
        h = bytes_list[ : Packet.HEAD_SIZE]
        message_type = h[0]

        #Lembrando que:
        # 0 – tipo de mensagem
        # h1 – livre
        # h2 – livre
        # h3 – número total de pacotes do arquivo
        # h4 – número do pacote sendo enviado
        # h5 – se tipo for handshake: id do arquivo
        # h5 – se tipo for dados: tamanho do payload
        # h6 – pacote solicitado para recomeço quando a erro no envio.
        # h7 – último pacote recebido com sucesso.
        # h8 – h9 – CRC

        eop = [b'\xAA', b'\xBB', b'\xCC', b'\xDD']
        # É preciso checar se o eop está no lugar certo. Retorna falso caso contrário
        if eop[-1]==bytes_list[-1] and eop[-2]==bytes_list[-2] and eop[-3]==bytes_list[-3] and eop[-4]==bytes_list[-4]:
            match message_type:
                case b'\x01': packet = Type1(int.from_bytes(h[5], byteorder="big"), int.from_bytes(h[3], byteorder="big"))
                case b'\x02': packet = Type2(int.from_bytes(h[5], byteorder="big"))
                case b'\x03':
                    payload_bytes = utils.splitBytes(raw_packet[Packet.HEAD_SIZE: -1* Packet.EOP_SIZE])
                    payload_int = []
                    for byte in payload_bytes:
                        payload_int.append(byte)
                    packet = Type3(int.from_bytes(h[3], byteorder="big"), int.from_bytes(h[4], byteorder="big"), payload_bytes)
                case b'\x04': packet = Type4(int.from_bytes(h[7], byteorder= "big"))
                case b'\x05': packet = Type5()
                case b'\x06': packet = Type6(int.from_bytes(h[6], byteorder="big"))
                case _: packet = False
        else: return False

        # Testando o crc
        calc_crc = utils.splitBytes(Crc16.calc(packet.bytes_raw).to_bytes(Packet.CRC_SIZE, byteorder="big"))
        if calc_crc != packet.crc:
            print("CRC é diferente do esperado!")
            return False

        return packet
    
    @staticmethod
    def getROPSize(raw_head:list):
        """
        Retorna o tamanho do resto do pacote (Rest Of Packet) através do head
        Se não identificar o tipo da mensagem, retorna False
        """
        # Separando a lista de bytes
        bytes_head_list = utils.splitBytes(raw_head)
        # Verificando o tipo de mensagem. Apenas tipo 3 tem payload
        non_data_packets = [b'\x01', b'\x02' , b'\x04', b'\x05', b'\x06']
        if bytes_head_list[0] in non_data_packets:
            payload_size = 0
        elif bytes_head_list[0] == b'\x03':
            payload_size = int.from_bytes(bytes_head_list[5],byteorder="big")
            
        # Caso não seja identificado nenhum tipo no head, há erro de pacote
        # Enviando false para comunicar problema
        else: return False
        rop_size = payload_size + Packet.EOP_SIZE
        return rop_size

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
        self.server_id = server_id
        # O número do pacote de handshake é sempre 0
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

        super().__init__(head=head, payload=payload)

class Type2(Packet):
    """
    Classe para padronizar mensagens do tipo 2

    Enviada pelo servidor ao cliente, após o primeiro receber uma 
    mensagem tipo 1 com o número identificador correto

    Propriedades:
    - message_type: tipo de mensagem 
    - client_id: id do receptor do pacote

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
    - payload_size: tamanho do payload

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