from django.shortcuts import render
from django.http import HttpResponse

from rules_adding import forms 
from rules_fetcher_display.models import prerouting,postrouting,ServerDetails
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from z_python_scripts.ip_add_delete import ip_add
from django.contrib import messages
from rules_adding.models import LastPK
from django.db.models import Max

from django.db import connection


#from z_python_scripts import ip_add_delete

def tables_gen_add(routing,sourceip,sourceport=None,protocol=None,destinationip=None,destinationport=None,policy_id=None):
    if routing == "prerouting":
        tables="iptables -t nat -A PREROUTING -m comment --comment policy-{} -d {} -p {} -m {} --dport {} -j DNAT --to-destination {}:{}".format(policy_id,sourceip,protocol,protocol,sourceport,destinationip,destinationport)
        return tables
    elif routing == "postrouting":
        tables="iptables -t nat -A POSTROUTING -m comment --comment policy-{} -d {} -j SNAT --to-source {}".format(policy_id,destinationip,sourceip)
        return tables
    elif routing == "both":
        print(routing)
        tables="iptables -t nat -A PREROUTING -m comment --comment policy-{} -d {} -p {} -m {} --dport {} -j DNAT --to-destination {}:{}".format(policy_id,sourceip,protocol,protocol,sourceport,destinationip,destinationport)
        print(tables)
        tables2="iptables -t nat -A POSTROUTING -m comment --comment policy-{} -d {} -j SNAT --to-source {}".format(policy_id,destinationip,sourceip)
        print(tables2)
        return tables,tables2

def get_last_pks(routing):
    get_last_pk_record, created = LastPK.objects.get_or_create(pk=1)
    if routing == "prerouting" or routing == "preroute":
        return get_last_pk_record.prerouting_last_pk
            
    elif routing == "postrouting" or routing == "postroute":
        return get_last_pk_record.postrouting_last_pk
    elif routing == "both":
        return get_last_pk_record.prerouting_last_pk, get_last_pk_record.postrouting_last_pk
    

# Create your views here.
@never_cache
@login_required
@permission_required('rules_fetcher_display.edit')
def add(request):
   ops=ServerDetails.objects.get(pk=1)
   print(ops.ip)
   print(ops.username)
   print(ops.password)
   if request.method == "POST":
      routing = request.POST.get('routing')

      if routing == "prerouting": 
        form = forms.preform(request.POST) 
      elif routing == "postrouting":
          form = forms.postform(request.POST)
      else:
          form = forms.preform(request.POST)

      if form.is_valid():
               
               server_data=[]
               server_data2=[]
               data = form.cleaned_data
               routing=data['routing']
               if routing == "prerouting":  
                    max_prerouting_pk = prerouting.objects.all().aggregate(Max('pk'))['pk__max']
                    last_pk_pre_check, created = LastPK.objects.get_or_create(pk=1)

                    if last_pk_pre_check.prerouting_last_pk is None or last_pk_pre_check.prerouting_last_pk == 0:
                        previous_object_id_pre = get_last_pks(routing) + 1
                        last_pk_pre_check.prerouting_last_pk = previous_object_id_pre
                        print('pre_check0', previous_object_id_pre)

                    elif last_pk_pre_check.prerouting_last_pk == max_prerouting_pk:
                        previous_object_id_pre = get_last_pks(routing)+1
                        last_pk_pre_check.prerouting_last_pk = previous_object_id_pre 
                        print('pre_check', previous_object_id_pre)

                    else:
                        previous_object_id_pre = get_last_pks(routing) + 1
                        last_pk_pre_check.prerouting_last_pk = previous_object_id_pre
                        print('pre_check1', previous_object_id_pre)

                    last_pk_pre_check.save()
                    server_data.extend([
                            form.cleaned_data['routing'],
                            form.cleaned_data['source_ip'],
                            form.cleaned_data['source_port'],
                            form.cleaned_data['protocol'],
                            form.cleaned_data['destination_ip'],
                            form.cleaned_data['destination_port']
                            ])
                    
                    cmd=tables_gen_add(routing=server_data[0],sourceip=server_data[1],sourceport=server_data[2],protocol=server_data[3],destinationip=server_data[4],destinationport=server_data[5],policy_id=previous_object_id_pre)
                    
                    #print(routing,ops.ip,ops.username,"wZbGBZy1y5",cmd,policyid,server_data[1])
                    print(cmd)
                    prerouting.objects.get_or_create(**data)
                    '''
                    error_pre=ip_add(routing,ops.ip,ops.username,"wZbGBZy1y5",cmd,policyid,server_data[1])
                    if error_pre is not None and len(error_pre) > 1 and error_pre[1]:
                            print("returned error: {} with error code: {}".format(error_pre[0].strip("\n"), error_pre[1]))
                            error_msg="returned error: {} with error code: {}".format(error_pre[0].strip("\n"), error_pre[1])
                            request.session['error_msg'] = error_msg
                
                    else:
                        prerouting.objects.get_or_create(**data)
'''

               elif routing == "postrouting":
                    max_postrouting_pk = postrouting.objects.all().aggregate(Max('pk'))['pk__max']
                    last_pk_post_check, created = LastPK.objects.get_or_create(pk=1)

                    if last_pk_post_check.postrouting_last_pk is None or last_pk_post_check.postrouting_last_pk == 0:
                        previous_object_id_post = get_last_pks(routing) + 1
                        last_pk_post_check.postrouting_last_pk = previous_object_id_post
                        print('check0', previous_object_id_post)

                    elif last_pk_post_check.postrouting_last_pk == max_postrouting_pk:
                        previous_object_id_post = get_last_pks(routing)+1
                        last_pk_post_check.postrouting_last_pk = previous_object_id_post 
                        print('check2', previous_object_id_post)

                    else:
                        previous_object_id_post = get_last_pks(routing) + 1
                        last_pk_post_check.postrouting_last_pk = previous_object_id_post
                        print('check1', previous_object_id_post)

                    last_pk_post_check.save()




                    postrouting.objects.get_or_create(source_ip=data['destination_ip'], destination_ip=data['source_ip'], routing=data['routing'])
                    server_data.extend([
                                form.cleaned_data['routing'],
                                form.cleaned_data['source_ip'],
                                form.cleaned_data['destination_ip']
                                ])
                    cmd2=tables_gen_add(routing=server_data[0],sourceip=server_data[1],destinationip=server_data[2],policy_id=previous_object_id_post)
                    print(cmd2)
                    #ip_add(routing,ops.ip,ops.username,"wZbGBZy1y5",cmd2)
               elif routing == "both":
                  print(routing)
                  ##PREROUTING BLOCK###
                  routing="prerouting"
                  max_prerouting_pk = prerouting.objects.all().aggregate(Max('pk'))['pk__max']
                  last_pk_pre_check, created = LastPK.objects.get_or_create(pk=1)

                  if last_pk_pre_check.prerouting_last_pk is None or last_pk_pre_check.prerouting_last_pk == 0:
                        previous_object_id_pre = get_last_pks(routing) + 1
                        last_pk_pre_check.prerouting_last_pk = previous_object_id_pre
                        print('pre_check0', previous_object_id_pre)

                  elif last_pk_pre_check.prerouting_last_pk == max_prerouting_pk:
                        previous_object_id_pre = get_last_pks(routing)+1
                        last_pk_pre_check.prerouting_last_pk = previous_object_id_pre 
                        print('pre_check', previous_object_id_pre)

                  else:
                        previous_object_id_pre = get_last_pks(routing) + 1
                        last_pk_pre_check.prerouting_last_pk = previous_object_id_pre
                        print('pre_check1', previous_object_id_pre)

                  last_pk_pre_check.save()
                  ##POSTROUTING BLOCK###
                  routing="postrouting"
                  max_postrouting_pk = postrouting.objects.all().aggregate(Max('pk'))['pk__max']
                  last_pk_post_check, created = LastPK.objects.get_or_create(pk=1)

                  if last_pk_post_check.postrouting_last_pk is None or last_pk_post_check.postrouting_last_pk == 0:
                        previous_object_id_post = get_last_pks(routing) + 1
                        last_pk_post_check.postrouting_last_pk = previous_object_id_post
                        print('check0', previous_object_id_post)

                  elif last_pk_post_check.postrouting_last_pk == max_postrouting_pk:
                        previous_object_id_post = get_last_pks(routing)+1
                        last_pk_post_check.postrouting_last_pk = previous_object_id_post 
                        print('check2', previous_object_id_post)

                  else:
                        previous_object_id_post = get_last_pks(routing) + 1
                        last_pk_post_check.postrouting_last_pk = previous_object_id_post
                        print('check1', previous_object_id_post)

                  last_pk_post_check.save()
                  
                  server_data.extend([
                        form.cleaned_data['routing'],
                        form.cleaned_data['source_ip'],
                        form.cleaned_data['source_port'],
                        form.cleaned_data['protocol'],
                        form.cleaned_data['destination_ip'],
                        form.cleaned_data['destination_port']
                        ])
                  
                  server_data2.extend([
                        form.cleaned_data['routing'],
                        form.cleaned_data['source_ip'],
                        form.cleaned_data['destination_ip']
                        ])
                  #cmd,cmd2 = tables_gen_add(routing=server_data[0],sourceip=server_data[1],sourceport=server_data[2],protocol=server_data[3],destinationip=server_data[4],destinationport=server_data[5])
                  routing="both"
                  previous_object_id=get_last_pks(routing)
                  previous_object_id_pre=previous_object_id[0]
                  previous_object_id_post=previous_object_id[1]

                  prerouting.objects.get_or_create(**data)
                  postrouting.objects.get_or_create(source_ip=data['destination_ip'], destination_ip=data['source_ip'], routing=data['routing'])
                  
                  print(previous_object_id_pre,previous_object_id_post)
                  cmd=tables_gen_add(routing="prerouting",sourceip=server_data[1],sourceport=server_data[2],protocol=server_data[3],destinationip=server_data[4],destinationport=server_data[5],policy_id=previous_object_id_pre)
                  cmd2=tables_gen_add(routing="postrouting",sourceip=server_data[1],destinationip=server_data[2],policy_id=previous_object_id_post)
                  print(cmd)
                  print(cmd2)
                  '''
                  error_both_pre=ip_add(routing,ops.ip,ops.username,"wZbGBZy1y5",cmd,previous_object_id_pre,server_data[1],route="pre")
                  print(error_both_pre)


                  error_both_post=ip_add(routing,ops.ip,ops.username,"wZbGBZy1y5",cmd2,route="post")
                  print(error_both_post)

                  if error_both_pre is not None and len(error_both_pre) > 1 and error_both_pre[1]:
                        print("returned error: {} with error code: {}".format(error_both_pre[0].strip("\n"), error_both_pre[1]))
                        error_msg="returned error: {} with error code: {}".format(error_both_pre[0].strip("\n"), error_both_pre[1])
                        request.session['error_msg'] = error_msg
                  else:
                       prerouting.objects.get_or_create(**data)
                       postrouting.objects.get_or_create(source_ip=data['destination_ip'], destination_ip=data['source_ip'], routing=data['routing'])
               '''
               
   return redirect('rules')








