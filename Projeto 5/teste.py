from crccheck.crc import Crc16
import utils
import math
from datagrams import *

local_imagem = "./Projeto 5/test_img.png"
raw_data = open(local_imagem, 'rb').read()
# Transformando dados em uma lista de bytes
data = utils.splitBytes(raw_data)
data_size = len(data)
ammount =  math.ceil(data_size / Packet.MAX_PAYLOAD_SIZE)
packet1 = Type1(0, ammount)
print(f'Pacote original: {packet1.bytes_raw}')
print(packet1.crc)
# packet1.setCRC(new_crc=[b'\x00', b'\x00'])
# print(f'Pacote alterado {packet1.bytes_raw}')
# r_packet = Packet.decode(packet1.bytes_raw)

