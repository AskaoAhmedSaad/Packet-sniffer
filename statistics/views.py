# packet sniffer log in elasticsearch
# Auther: Askao Ahmed Saad
from django.shortcuts import render
from django.http import HttpResponse
import elasticsearch
import os
import signal
import subprocess
from packet_sniffer_log_in_es.settings import index_name , type_name


'''
    get all destination addresses to get statistics of it's packets
'''
def destination_addresses_statistics(request):
    # create elastic seach object
    es = elasticsearch.Elasticsearch()
    # get search results with aggregations in destination address field to get
    # unique destination address and it's total packets count
    log_results = es.search(index_name, type_name,
        {
          "query": {"match_all": {}},
          "aggs": {
                "unique_destination_address": {
                  "terms": {
                    "field": "destination_address"
                  }
                }
            }
        })
    return render(request, 'destination_addresses_statistics.html',{'log_results':log_results})


'''
    get all source addresses to get statistics of it's packets
'''
def source_addresses_statistics(request):
     # create elastic seach object
    es = elasticsearch.Elasticsearch()
    # get search results with aggregations in source address field to get
    # unique source address and it's total packets count
    log_results = es.search(index_name, type_name,
        {
          "query": {"match_all": {}},
          "aggs": {
                "unique_source_address": {
                  "terms": {
                    "field": "source_address"
                  }
                }
            }
        })
    return render(request, 'source_addresses_statistics.html',{'log_results':log_results})


'''
    get days that have packets
'''
def days_statistics(request):
    # get search results with aggregations in datetime field to get
    # days that have packets and it's total packets count
    es = elasticsearch.Elasticsearch() # create elastic seach object
    log_results = es.search(index_name, type_name,
        {
            "query": {"match_all": {}},
            "aggs": {
                "days": {"date_histogram": {"field": "datetime", "interval": "day"}}
            }
        })
    # get the days and it's total packets count and append it to days_list
    days_list = []
    for doc in log_results['aggregations']['days']['buckets']:
        day_name = doc['key_as_string'].split('T')[0]
        day_key = doc['key_as_string'].split('T')[0].replace('-','_')
        days_list.append({'day_name' : day_name, 'day_key':  day_key, 'total_count' : doc['doc_count']})
    print days_list
    return render(request, 'days_statistics.html',{'days_list':days_list})


'''
    view total packets count for certain day
'''
def veiw_day_statistics(request, day):
    day_name = day.replace('_','-') #convert the day string format
    es = elasticsearch.Elasticsearch() # create elastic seach object
    # get search results with aggregations in datetime field with days to get
    # day total packets count
    log_results = es.search(index_name, type_name,
        {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "datetime": {
                                    "gt": day_name + "T00:00",
                                    "lt": day_name + "T23:59"
                                }
                            }
                        }
                    ],
                }
            },
            "aggs": {
                "days": {"date_histogram": {"field": "datetime", "interval": "hour"}}
            }
    })
    # get the day hours and it's total packets count and append it to hours_list
    hours_list = []
    for doc in log_results['aggregations']['days']['buckets']:
        hour_name = doc['key_as_string'].split('T')[1].split(':')[0]
        hours_list.append({'hour_name' : hour_name, 'total_count' : doc['doc_count']})
    print hours_list
    return render(request, 'veiw_day_statistics.html',{'hours_list':hours_list, 'day_name':day_name})
