from datagrams import *
import utils

packet1_IN = Type1(server_id=1, ammount=10)
print('\n \n')
print('--- '*20)
packet1_OUT = Packet.decode(packet1_IN.sendable)
if(packet1_OUT.bytes_list == packet1_IN.bytes_list): print('foi')
print(packet1_OUT.message_type, packet1_OUT.server_id)