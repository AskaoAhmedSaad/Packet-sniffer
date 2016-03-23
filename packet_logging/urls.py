from django.conf.urls import url, patterns
from . import views

urlpatterns = [
    url(r'^$', views.packet_sniffer_logger, name='packet_sniffer_logger'),
    url(r'single_param_search/', views.single_param_search, name='single_param_search'),
    url(r'multi_param_search/', views.multi_param_search, name='multi_param_search'),
    url(r'packet_sniffer_logger/', views.packet_sniffer_logger, name='packet_sniffer_logger'),
    url(r'start_sniffer/', views.start_sniffer, name='start_sniffer'),
    url(r'stop_sniffer/', views.stop_sniffer, name='stop_sniffer'),
]
