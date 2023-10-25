import paramiko
class SSH:

    def ssh_call(self,host,user,passwd,cmd):
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=passwd)
        _stdin, _stdout,_stderr = client.exec_command(cmd)
        output = _stdout.read().decode()
        output_error = _stderr.read().decode()
        client.close()
        return output

