#!/usr/bin/env python3

import paramiko 
from scp import SCPClient
import sys
import os

host = 'rpi4print.wysechoice.net'
user = 'pi'
pw = '<store securely outside the repository>'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname = host, port = '22', username = user, password = pw)
dirname = '/tmp/' + os.path.dirname(sys.argv[1])

sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
try:
    sftp.mkdir(dirname)
except:
	pass
sftp.close()

scp = SCPClient(ssh.get_transport())
scp.put(sys.argv[1], dirname)
scp.close()

# Should now be printing the current progress of your put function.
ssh.exec_command("/usr/bin/ptouch-print --image /tmp/" + sys.argv[1])

ssh.close()