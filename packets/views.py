# packet sniffer log in elasticsearch
# Auther: Askao Ahmed Saad
from django.shortcuts import render
from django.http import HttpResponse
from classes.repositories.GetPacketsRepository import searchPackets
import os
import signal
import subprocess

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
    log_results = searchPackets(request)
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
