import paramiko
from scp import SCPClient
from config import *
import os


def create_ssh_client():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(REMOTE_SSH_SERVER, 22, REMOTE_SSH_USER)
    return client


def create_folder(folder):
    ssh = create_ssh_client()
    scp = SCPClient(ssh.get_transport())

    # folder , repository/scorm
    os.makedirs(folder)
    scp.get(
        '%simsmanifest.xml' % folder,
        folder
    )
    print 'imsmanifest.xml criado'
    scp.get(
            folder[:-1],
            '/var/www/html/moodle3.1/moodledata/repository/scorm/',
            recursive=True
    )
    print 'conteudo do scorm copiado'

    scp.close()