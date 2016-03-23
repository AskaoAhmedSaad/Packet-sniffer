'''
    add packets as a documents in elasticsearch index
'''
# Auther: Askao Ahmed Saad
import elasticsearch
from datetime import datetime

es = elasticsearch.Elasticsearch()

index_name = "my_index"
type_name = "my_type"


def add_packet(version, ip_header_length, ttl, protocol, source_address, destination_address, source_port, dest_port,
    sequence_number, acknowledgement, tcp_header_length, data, datetime):
    try: # try to add packet
        es.index(index="my_index", doc_type="my_type",
         body={
            "version":version,
            "ip_header_length":ip_header_length,
            "ttl":ttl,
            "protocol":protocol,
            "source_address":source_address,
            "destination_address":destination_address,
            "source_port":source_port,
            "dest_port":dest_port,
            "sequence_number":sequence_number,
            "acknowledgement":acknowledgement,
            "tcp_header_length":tcp_header_length,
            "data":data,
            "datetime":datetime
            })
    except: # if there is exception in adding packet data as encrypted data drop this data
        es.index(index="my_index", doc_type="my_type",
         body={
            "version":version,
            "ip_header_length":ip_header_length,
            "ttl":ttl,
            "protocol":protocol,
            "source_address":source_address,
            "destination_address":destination_address,
            "source_port":source_port,
            "dest_port":dest_port,
            "sequence_number":sequence_number,
            "acknowledgement":acknowledgement,
            "tcp_header_length":tcp_header_length,
            "data":'',
            "datetime":datetime
            })
