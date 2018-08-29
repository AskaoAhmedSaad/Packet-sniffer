# Packet sniffer log in elasticsearch

django web application sniff network packets over tcp protocol, log in elasticsearch index, single and multi params search for packets, statistics and charts for packets


**requirements**<br>
- django 1.11.12
- pyes python models
- elasticsearch-6.2.3


**Running the application**<br><br>
- firstly run es_mapping.py script to create elasticesearch index, type and mapping:<br>
`python es_mapping.py`
<br>
- migrate django models to db because we need django_session model:<br>
`python manage.py migrate`
<br>
- run the project with root permision to run the packet sniffer and logging script:<br>
`sudo python manange.py runserver`
<br>
- you can run packet sniffer and logging script separetly:<br>
`sudo python packet_sniffer.py`


  ![print screen](https://www.mediafire.com/convkey/8a67/sub8ju81bwp8y4o6g.jpg)
