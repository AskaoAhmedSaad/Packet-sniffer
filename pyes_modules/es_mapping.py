'''
    create elasticesearch index, type and mapping
'''
# Auther: Askao Ahmed Saad
import elasticsearch

es = elasticsearch.Elasticsearch()
index_name = "my_index"
type_name = "my_type"

es.indices.delete(index_name) # delete the index if present
es.indices.create(index_name) # then create it
es.cluster.health(wait_for_status="yellow") #

# add mapping
es.indices.put_mapping(index=index_name, doc_type=type_name, body={"properties": {
    "version": {"type": "text", "fielddata": "true"},
    "ip_header_length": {"type": "text", "fielddata": "true"},
    "ttl": {"type": "text", "fielddata": "true"},
    "protocol": {"type": "text", "fielddata": "true"},
    "source_address": {"type": "text", "fielddata": "true"},
    "destination_address": {"type": "text", "fielddata": "true"},
    "source_port": {"type": "text", "fielddata": "true"},
    "dest_port": {"type": "text", "fielddata": "true"},
    "sequence_number": {"type": "text", "fielddata": "true"},
    "acknowledgement": {"type": "text", "fielddata": "true"},
    "tcp_header_length": {"type": "text", "fielddata": "true"},
    "data": {"type": "text", "fielddata": "true"},
    "datetime": {"type": "date"},
    }})

mappings = es.indices.get_mapping(index_name, type_name)
