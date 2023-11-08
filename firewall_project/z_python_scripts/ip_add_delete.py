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
 
def del_pol(types,ip=None,username=None,password=None,cmd=None,policy_id=None,destinationip=None):
   '''
    command_d=f"ifconfig bond0-{policy_id} down"
    op_d,exit_status_d=ssh_call("10.0.2.15","root","notu",command_d)
    if exit_status_d == 0:
       command_d = f"rm -rf /etc/network/interfaces.d/bond0-{policy_id}"
       ssh_call("10.0.2.15","root","notu",command_d)
   '''
   if types == "postroute":
      del_check_cmd="iptables -t nat -L POSTROUTING | awk '{print $5}' | grep -i {} | wc -l".format(destinationip)
      print(del_check_cmd)
      print(ip,username,destinationip)
      del_check=ssh_call(ip,username,"notu",[del_check_cmd])
      print("error",del_check)
      print(del_check[0].strip('\n')[0])
      if int(del_check[0].strip('\n')[0]) > 0:
          ssh_call(ip,username,password,[cmd])

          
          

