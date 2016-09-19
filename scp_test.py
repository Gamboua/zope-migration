import paramiko
from scp import SCPClient
from config import *


def create_ssh_client():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(REMOTE_SSH_SERVER, 22, REMOTE_SSH_USER)
    return client


def create_folder():
    ssh = create_ssh_client()
    scp = SCPClient(ssh.get_transport())

    print scp

    scp.close()


create_folder()