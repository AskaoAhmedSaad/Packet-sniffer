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
    "version": {"index": "analyzed", "type": "string", "store": "yes", "term_vector": "with_positions_offsets"},
    "ip_header_length": {"index": "analyzed", "type": "string", "store": "yes", "term_vector": "with_positions_offsets"},
    "ttl": {"index": "analyzed", "type": "string", "store": "yes", "term_vector": "with_positions_offsets"},
    "protocol": {"index": "analyzed", "type": "string", "store": "yes", "term_vector": "with_positions_offsets"},
    "source_address": {"index": "analyzed", "type": "string", "store": "yes", "term_vector": "with_positions_offsets"},
    "destination_address": {"index": "analyzed", "type": "string", "store": "yes", "term_vector": "with_positions_offsets"},
    "source_port": {"index": "analyzed", "type": "string", "store": "yes", "term_vector": "with_positions_offsets"},
    "dest_port": {"index": "analyzed", "type": "string", "store": "yes", "term_vector": "with_positions_offsets"},
    "sequence_number": {"index": "analyzed", "type": "string", "store": "yes", "term_vector": "with_positions_offsets"},
    "acknowledgement": {"index": "analyzed", "type": "string", "store": "yes", "term_vector": "with_positions_offsets"},
    "tcp_header_length": {"index": "analyzed", "type": "string", "store": "yes", "term_vector": "with_positions_offsets"},
    "data": {"index": "analyzed", "type": "string", "store": "yes", "term_vector": "with_positions_offsets"},
    "datetime": {"index": "analyzed", "type": "date", "store": "yes"},
    }})

mappings = es.indices.get_mapping(index_name, type_name)
