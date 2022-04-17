from app_client import *

# Dados a serem transmitidos (bytes da imagem "test_img.png")
local_imagem = "./Projeto 4 (Teste)/test_img.png"
raw_data = open(local_imagem, 'rb').read()
# Transformando dados em uma lista de bytes
data = utils.splitBytes(raw_data)
data_size = len(data)
ammount =  math.ceil(data_size / Packet.MAX_PAYLOAD_SIZE)


