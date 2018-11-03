from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.packet_sniffer_logger, name='packet_sniffer_logger'),
    url(r'search/', views.search, name='search'),
    url(r'packet_sniffer_logger/', views.packet_sniffer_logger, name='packet_sniffer_logger'),
    url(r'start_sniffer/', views.start_sniffer, name='start_sniffer'),
    url(r'stop_sniffer/', views.stop_sniffer, name='stop_sniffer'),
]
