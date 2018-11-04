''' Packet sniffer in python for Linux sniffs only
    incoming TCP packet and logged in elasticesearch index
'''
import socket, sys
from struct import *
from pyes_modules.logging_packets import add_packet
import datetime

# create socket
try:
    s = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_IP)
except socket.error , msg:
    print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# receive a packet
while True:
    packet = s.recvfrom(65565)
    #packet string from tuple
    packet = packet[0]
    #take first 20 characters for the ip header
    ip_header = packet[0:20]
    #now unpack them :)
    iph = unpack('!BBHHHBBH4s4s' , ip_header)
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    iph_length = ihl * 4
    s_addr = socket.inet_ntoa(iph[8]);
    d_addr = socket.inet_ntoa(iph[9]);
    if (s_addr != '127.0.0.1' && d_addr != '127.0.0.1'):
        ttl = iph[5]
        protocol = iph[6]
        tcp_header = packet[iph_length:iph_length+20]
        #now unpack them :)
        tcph = unpack('!HHLLBBHHH' , tcp_header)
        source_port = tcph[0]
        dest_port = tcph[1]
        sequence = tcph[2]
        acknowledgement = tcph[3]
        doff_reserved = tcph[4]
        tcph_length = doff_reserved >> 4
        h_size = iph_length + tcph_length * 4
        data_size = len(packet) - h_size
        #get data from the packet
        data = packet[h_size:]

        # print packet paras
        print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)
        print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
        print 'Data : ' + data

        # log the packet in es document
        add_packet(str(version), str(ihl), str(ttl), str(protocol), str(s_addr),
          str(d_addr), str(source_port), str(dest_port) , str(sequence), str(acknowledgement), str(tcph_length), str(data), datetime.datetime.now())
