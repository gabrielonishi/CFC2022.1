from crccheck.crc import Crc16
from numpy import asarray
import utils
import math
from datagrams import *

local_imagem = "./Projeto 5/test_img.png"
raw_data = open(local_imagem, 'rb').read()
data = utils.splitBytes(raw_data)
data_size = len(data)
ammount =  math.ceil(data_size / Packet.MAX_PAYLOAD_SIZE)
sent_packet_1 = Type3(ammount, 1, data[:Packet.MAX_PAYLOAD_SIZE])
received_packet_1 = Packet.decode(sent_packet_1.sendable)
print(sent_packet_1.sendable)
print('what')
print(received_packet_1.sendable)