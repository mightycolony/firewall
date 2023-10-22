import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','firewall_project.settings')

import django
django.setup()

from rules_fetcher_display.models import prerouting,postrouting
import numpy as np

with open("iptables") as f:
    mylist = f.read().splitlines()

output = np.array([elem.split(', ') for elem in mylist])
nested_list = output.tolist()
def rule():
    previous_ip=""
    previous_source_port=""
    previous_destination_port=""
    for i in range(0, len(mylist)):
        rules_values = nested_list[i]
        a = [j.split(' ') for j in rules_values]
        routing = a[0][1]
        if routing == "PREROUTING":
            source_ip = a[0][3]
            protocol = a[0][5]
            source_port = a[0][9]
            destination = a[0][13]
            destination_ip = destination.split(':')[0]
            destination_port = destination.split(':')[1]
            existing = None
            print("pre",previous_ip)
            if previous_ip == source_ip:
              print("port",source_port)
              new_source_port=source_port + "|" +previous_source_port
              new_destination_port=destination_port + "|" + previous_destination_port

              existing=prerouting.objects.filter(source_ip=previous_ip).update(
                            routing=routing,
                            source_ip=source_ip,
                            protocol=protocol,
                            source_port=new_source_port,
                            destination_ip=destination_ip,
                            destination_port=new_destination_port
              )
            else:
                try:
                   prerouting.objects.get(source_ip=source_ip)
                except prerouting.DoesNotExist:

                 source_ip = a[0][3]
                 print("esleport",source_port)
                 prerouting.objects.get_or_create(routing=routing,source_ip=source_ip,protocol=protocol,source_port=source_port,destination_ip=destination_ip,destination_port=destination_port)
                
                



        previous_ip = source_ip
        previous_source_port=source_port
        previous_destination_port=destination_port

        if routing == "POSTROUTING":
            source_ip = a[0][3]
            destination_ip = a[0][7]
            post=postrouting.objects.get_or_create(routing=routing,source_ip=source_ip,destination_ip=destination_ip)
rule()
