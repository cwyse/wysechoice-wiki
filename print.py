#!/usr/bin/env python3

import paramiko 
from scp import SCPClient
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname = '192.168.1.119', port = '22', username = 'pi', password = '<store securely outside the repository>')

scp = SCPClient(ssh.get_transport())
scp.put('labels/2020.0040_Ilex_serrata_Koshobai.png', '/tmp')

# Should now be printing the current progress of your put function.
ssh.exec_command("ptouch-print --image /tmp/2020.0040_Ilex_serrata_Koshobai.png")

scp.close()
