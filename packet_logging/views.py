# packet sniffer log in elasticsearch
# Auther: Askao Ahmed Saad
from django.shortcuts import render
from django.http import HttpResponse
from pyes import ES
import elasticsearch
from pyes.query import *
from pyes.filters import *
import os
import signal
import subprocess
from packet_sniffer_log_in_es.settings import index_name , type_name


def packet_sniffer_logger(request):
    '''
        start and stop packet sniffing, call packet_sniffer script that
        sniffs network packets and logs it in elasticsearch documents
    '''
    return render(request, 'packet_sniffer_logger.html')


def single_param_search(request):
    '''
        search in elasticsearch packet documents with single param
    '''
    log_results = None
    es = ES() # create elastic seach object
    if request.method == 'POST': # if the search form is submitted
        # filter with search param and search tearm
        q1 = TermFilter(request.POST.get('searchby'), request.POST.get('searchterm'))
        orq = ORFilter([q1])
        q = FilteredQuery(MatchAllQuery(), orq)
        log_results = es.search(q, indices=index_name, doc_types=type_name) # get the filtered data from elasticsearch
    elif request.method == 'GET': # get all packet when get the search page
        log_results = es.search(MatchAllQuery(), indices=index_name, doc_types=type_name)
    return render(request, 'single_param_search.html',{'log_results':log_results})


def multi_param_search(request):
    '''
        search in elasticsearch packet documents with multi param
    '''
    log_results = None
    es = ES() # create elastic seach object
    if request.method == 'POST': # if the search form is submitted
        filters_list = []
        # loop on each search param and check if it has value to add it to filter list
        for param in ["version","ip_header_length","ttl","protocol","source_address","destination_address",
            "source_port","dest_port","sequence_number", "acknowledgement", "tcp_header_length", "data", "datetime"]:
            if request.POST.get(param) != '':
                q_param = TermFilter(param, request.POST.get(param))
                filters_list.append(q_param)
        if len(filters_list) != 0: # if there is filter params  get the results
            orq = ANDFilter(filters_list)
            q = FilteredQuery(MatchAllQuery(), orq)
            log_results = es.search(q, indices=index_name, doc_types=type_name)
        else:
            log_results = None
    elif request.method == 'GET': # get all packet when get the search page
        log_results = es.search(MatchAllQuery(), indices=index_name, doc_types=type_name)
    return render(request, 'multi_param_search.html',{'log_results':log_results})


def start_sniffer(request):
    '''
        start packet_sniffer script
    '''
    # start packet_sniffer script as system proccess
    proc = subprocess.Popen(['python', 'packet_sniffer.py'], stdout=subprocess.PIPE,
                       shell=False, preexec_fn=os.setsid)
    print "PID:", proc.pid
    #store proccess id in the session
    request.session['PID'] = proc.pid
    return HttpResponse('startted')


def stop_sniffer(request):
    '''
        stop packet_sniffer script
    '''
    # if the process id pressent as session variable kill this process
    if 'PID' in request.session:
        print request.session['PID']
        os.killpg(os.getpgid(int(request.session['PID'])), signal.SIGTERM)  # Send the signal to all the process groups
        # then delete PID session variable
        del request.session['PID']
    return HttpResponse('stopped')
