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
              print("Authentication failed.")
        except paramiko.SSHException:
             print("SSH connection failed.")
        except Exception as e:
              print(f"An error occurred: {str(e)}")
        finally:
           client.close()
        return output_list
            
def ip_add(routing,ip,user_name,password,cmd,policy_id="None",source_ip="None",precmd="None",postcmd="None"):
   
        
    if routing == "prerouting":
         content = f"auto bond0:{policy_id}\n\tiface bond0:{policy_id} inet static\n\taddress {source_ip}\n\tnetmask 255.255.255.0\n\tgateway 192.168.1.1"
         command_check=f"ip a | grep -i {source_ip} | awk -F ' ' '{{print $2}}'"
         checker=ssh_call(ip,user_name,password,[command_check])
         checker_op=checker[0].strip('\n').split('/')[0]
         #checker_op==checker[0].strip('\n')  #org_one with subnet
         if checker_op != ip:
            command1 = f"echo '{content}' | tee /etc/network/interfaces.d/bond0-{policy_id} > /dev/null"
            command2=f"ifconfig bond0-{policy_id} up"
            commands=[command1,command2,cmd]
            op=ssh_call(ip,user_name,password,commands)
            return op
            
    elif routing == "postrouting":
        op=ssh_call(ip,user_name,password,[cmd])
        print(op)
    elif routing == "both":
         if precmd == "cmd":
             content = f"auto bond0:{policy_id}\n\tiface bond0:{policy_id} inet static\n\taddress {source_ip}\n\tnetmask 255.255.255.0\n\tgateway 192.168.1.1"
             command_check=f"ip a | grep -i {source_ip} | awk -F ' ' '{{print $2}}'"
             checker=ssh_call(ip,user_name,password,[command_check])
             checker_op=checker[0].strip('\n').split('/')[0]
             #checker_op==checker[0].strip('\n')  #org_one with subnet
             if checker_op != ip:
                command1 = f"echo '{content}' | tee /etc/network/interfaces.d/bond0-{policy_id} > /dev/null"
                command2=f"ifconfig bond0-{policy_id} up"
                commands=[command1,command2,cmd]
                op=ssh_call(ip,user_name,password,commands)
                return op
         elif postcmd == "cmd2":
            op_both=ssh_call(ip,user_name,password,[cmd])
            print(op_both)
         

'''
def del_add(policy_id):

    command_d=f"ifconfig bond0-{policy_id} down"
    op_d,exit_status_d=ssh_call("10.0.2.15","root","notu",command_d)
    if exit_status_d == 0:
       command_d = f"rm -rf /etc/network/interfaces.d/bond0-{policy_id}"
       ssh_call("10.0.2.15","root","notu",command_d)

'''