# packet sniffer log in elasticsearch
# Auther: Askao Ahmed Saad
from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch
import os
import signal
import subprocess
from packet_sniffer_log_in_es.settings import index_name, type_name


'''
    start and stop packet sniffing, call packet_sniffer script that
    sniffs network packets and logs it in elasticsearch documents
'''
def packet_sniffer_logger(request):
    return render(request, 'packet_sniffer_logger.html')

'''
    search in elasticsearch packet documents with multi param
'''
def search(request):
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
    return render(request, 'search.html',{'log_results':log_results})


'''
    start packet_sniffer script
'''
def start_sniffer(request):
    # start packet_sniffer script as system proccess
    proc = subprocess.Popen(['python', 'packet_sniffer.py'], stdout=subprocess.PIPE,
                       shell=False, preexec_fn=os.setsid)
    print "PID:", proc.pid
    #store proccess id in the session
    request.session['PID'] = proc.pid
    return HttpResponse('startted')


'''
    stop packet_sniffer script
'''
def stop_sniffer(request):
    # if the process id pressent as session variable kill this process
    if 'PID' in request.session:
        print request.session['PID']
        os.killpg(os.getpgid(int(request.session['PID'])), signal.SIGTERM)  # Send the signal to all the process groups
        # then delete PID session variable
        del request.session['PID']
    return HttpResponse('stopped')
