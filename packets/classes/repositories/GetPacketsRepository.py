from elasticsearch import Elasticsearch
from packet_sniffer_log_in_es.settings import index_name, type_name

def searchPackets(request):
    es = Elasticsearch()
    if request.method == 'POST': # if the search form is submitted
        filters_dic = {}
        # loop on each search param and check if it has value to add it to filter list
        for param in ["version","ip_header_length","ttl","protocol","source_address","destination_address",
            "source_port","dest_port","sequence_number", "acknowledgement", "tcp_header_length", "data", "datetime"]:
            if request.POST.get(param) != '':
                filters_dic[param] = request.POST.get(param)
        if len(filters_dic) != 0: # if there is filter params  get the results
            data = es.search(index=index_name, doc_type=type_name, body={"query": {"match": filters_dic}})
        else:
            data = None
    elif request.method == 'GET': # get all packet when get the search page
        data = es.search(index=index_name, doc_type=type_name, body={"query": {"match_all": {}}})
    log_results = data['hits']['hits'] if data is not None else None

    return log_results
