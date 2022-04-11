from datagrams import *

def splitBytes(data):
    """
    Transforma um conjunto de dados em uma lista de bytes
    """
    split_data = [data[i:i + 1] for i in range(0, len(data), 1)]
    result = list()
    for data in split_data:
        result.append(bytes(data))
    return result

def decode(raw_packet):
        '''
        Retorna um objeto Packet a partir de uma lista de bytes de um datagrama recebido
        Retorna False se receber um pacote com especificações inesperadas
    
        Parâmetros:
        - message_type: tipo de mensagem esperada
        - raw_datagram: dados brutos que seguem o formato do datagrama

        '''

        # extrai o HEAD e o EOP
        bytes_list = splitBytes(raw_packet)
        head = bytes_list[ : Packet.HEAD_SIZE]
        message_type = head[0]

        #Lembrando que:
        # 0 – tipo de mensagem
        # h1 – livre
        # h2 – livre
        # h3 – número total de pacotes do arquivo
        # h4 – número do pacote sendo enviado
        # h5 – se tipo for handshake:id do arquivo
        # h5 – se tipo for dados: tamanho do payload
        # h6 – pacote solicitado para recomeço quando a erro no envio.
        # h7 – último pacote recebido com sucesso.
        # h8 – h9 – CRC

        match message_type:
            case 1:Type1(head[5], head[3])
            case 2:Type2()
            case 3:Type3(head[3], head[4], bytes_list[Packet.HEAD_SIZE + 1: -1 * Packet.EOP_SIZE -1])
            case 4:Type4(head[7])
            case 5:Type5()
            case 6:Type6(head[6])
        
        eop = bytes_list[-1 * Packet.EOP_SIZE : ]


def tryAgainPrompt():

    while True:

        answer = input("Tentar novamente? S/N\n")
        if answer.upper() == "N": return False
        elif answer.upper() == "S": return True
        else: print("Não entendi.\n")

local_imagem = "./Projeto 4/test_img.png"
txBuffer = open(local_imagem, 'rb').read()
print(txBuffer)
print(splitBytes(txBuffer))