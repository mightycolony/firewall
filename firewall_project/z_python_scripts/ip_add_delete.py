import paramiko
def ssh_call(host,user,passwd,commands):

        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        output_list=[]
        try:
            for command in commands:
                client.connect(host, username=user, password=passwd)
                _stdin, _stdout,_stderr = client.exec_command(command)
                output=_stdout.read().decode()
                output_err = _stderr.read().decode()
                exit_status = _stdout.channel.recv_exit_status()
                output_list=[output,output_err,exit_status]
                if exit_status != 0:
                     break
                    
            

        except paramiko.AuthenticationException:
              return "Authentication failed."
        except paramiko.SSHException:
             return "SSH connection failed."
        except Exception as e:
              return f"An error occurred: {str(e)}"
        finally:
           client.close()
        return output_list
            
def ip_add(routing,ip,user_name,password,cmd,policy_id="None",source_ip="None",route="None"):
   
        
    if routing == "prerouting":
         content = f"auto enp0s3:{policy_id}\niface enp0s3:{policy_id} inet static\n\taddress {source_ip}\n\tnetmask 255.255.255.0"
         command_check=f"ip a | grep -i {source_ip} | awk -F ' ' '{{print $2}}'"
         print("login",ip,user_name,password)
         checker=ssh_call(ip,user_name,password,[command_check])
         print(checker)
         checker_op=checker[0].strip('\n').split('/')[0]
         print(checker_op)
         #checker_op = checker[0].strip('\n')  #org_one with subnet
         if source_ip not in checker_op:
            command1 = f"echo '{content}' | tee /etc/network/interfaces.d/enp0s3:{policy_id} > /dev/null"
            command2=f"ip link set enp0s3:{policy_id}; ifup enp0s3:{policy_id} "
            commands=[command1,command2,cmd]
            op=ssh_call(ip,user_name,password,commands)
            return op
         else:
            else_op=ssh_call(ip,user_name,password,[cmd])
            return else_op
         
    elif routing == "postrouting":
        op=ssh_call(ip,user_name,password,[cmd])
        print(op)
          
    elif routing == "both":
         print(route)
         if route == "pre":
             content = f"auto enp0s3:{policy_id}\n\tiface enp0s3:{policy_id} inet static\n\taddress {source_ip}\n\tnetmask 255.255.255.0"
             print(source_ip)
             command_check=f"ip a | grep -i {source_ip} | awk -F ' ' '{{print $2}}'"
             print("cmd_check",command_check)
             checker=ssh_call(ip,user_name,password,[command_check])
             checker_op=checker[0].strip('\n').split('/')[0]
             #checker_op==checker[0].strip('\n')  #org_one with subnet
             if source_ip not in checker_op:
                command1 = f"echo '{content}' | tee /etc/network/interfaces.d/enp0s3:{policy_id} > /dev/null"
                command2=f"ip link set enp0s3:{policy_id}; ifup enp0s3:{policy_id} "

                commands=[command1,command2,cmd]
                op=ssh_call(ip,user_name,password,commands)
                return op
         elif route == "post":
            else_op=ssh_call(ip,user_name,password,[cmd])
            return else_op
 
def del_pol(types,ip=None,username=None,password=None,cmd=None,policy_id=None,sourceip=None,destinationip=None):
   '''
    
   '''
   if types == "preroute":
      del_check_cmd="iptables -t nat -L PREROUTING | awk '{{print $5}}' | grep -v -e 'destination' -e '^$' | wc -l".format(sourceip) 
      op=ssh_call(ip,username,password,[del_check_cmd])
      print("error",op)
      print(op[0].strip('\n')[0])
      if int(op[0].strip('\n')[0]) == 1:
         policy_from_ipa=f"ip a  | grep {sourceip} | awk '{{print $NF}}'"
         print(policy_from_ipa)
         id=ssh_call(ip,username,password,[policy_from_ipa])
         pol_id=id[0].strip('\n')
         command_d = f"ifdown {pol_id}; rm -rf /etc/network/interfaces.d/{pol_id}"
         del_cmd=ssh_call(ip,username,password,[command_d])
         print(del_cmd)
         print(pol_id)
      ssh_call(ip,username,password,[cmd])
      

   if types == "postroute":
      del_check_cmd="iptables -t nat -L POSTROUTING | grep -i policy-{} | wc -l".format(policy_id)
      print(del_check_cmd)
      print(ip,username,destinationip)
      del_check=ssh_call(ip,username,"notu",[del_check_cmd])
      print("error",del_check)
      print(del_check[0].strip('\n')[0])
      if int(del_check[0].strip('\n')[0]) > 0:
          ssh_call(ip,username,password,[cmd])

          
          

def save_pol(routing,ip=None,username=None,password=None,cmd=None,policy_id=None,sourceip=None,destinationip=None,sourceport=None,destinationport=None):
    if routing == "postrouting":
        rule_number_check="iptables -t nat -L POSTROUTING --line-numbers | grep 'policy-{}'| awk '{{print $1}}'".format(policy_id)
        rule_number=ssh_call(ip,username,password,[rule_number_check])
        
        rule_num=rule_number[0].strip('\n')
        print("rule_number",rule_num)
        save_rule="iptables -t nat -R POSTROUTING {} -m comment --comment 'policy-{}' -d  {} -j SNAT --to-source {}".format(rule_num,policy_id,destinationip,sourceip)
        print(save_rule)
        save_ops=ssh_call(ip,username,password,[save_rule])
        print(save_ops)




    if routing == "prerouting":
        rule_number_checks="iptables -t nat -L PREROUTING --line-numbers | grep 'policy-{}'| awk '{{print $1}}'".format(policy_id)
        rule_numbers=ssh_call(ip,username,password,[rule_number_checks])
        
        rule_nums=rule_numbers[0].strip('\n')
        print("rule_number",rule_nums)
        save_rules="iptables -t nat -R PREROUTING {} -m comment --comment 'policy-{}' -d {} -p tcp -m tcp --dport {} -j DNAT --to-destination {}:{}".format(rule_nums,policy_id,sourceip,sourceport,destinationip,destinationport)
        print(save_rules)
        save_opss=ssh_call(ip,username,password,[save_rules])
        print(save_opss)