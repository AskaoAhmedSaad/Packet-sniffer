from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'days_statistics/', views.days_statistics, name='days_statistics'),
    url(r'destination_addresses_statistics/', views.destination_addresses_statistics, name='destination_addresses_statistics'),
    url(r'source_addresses_statistics/', views.source_addresses_statistics, name='source_addresses_statistics'),
    url(r'veiw_day_statistics/(?P<day>\w+)/$', views.veiw_day_statistics, name='veiw_day_statistics'),
]
