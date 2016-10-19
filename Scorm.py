import paramiko
import os
from scp import SCPClient
from config import *
from Command import Command


class Scorm:

    def __init__(self, scorm, course):
        self.course = course
        self.scp = None

        self.type = 'scorm'
        self.section = 0

        self.folder = self.get_if_exists('folder', scorm)
        self.title = self.get_if_exists('title', scorm)

    def get_if_exists(self, parameter, json):
        return json.get(parameter) if parameter in json else None

    def scorm_add(self):
        self.scorm_import_folder()
        self.scorm_zip()
        Command.command_execute(Command.activity_create_command(
            options=self.get_scorm_options(), type=self.type, id=self.course.id
        ))

    def get_scorm_options(self):
        params = []
        if self.section is not None:
            params.append('--section %s' % self.section)
        if self.title:
            params.append('--name "%s"' % self.title)

        params.append('--filepath /tmp/scorm_dir.zip')

        return ' '.join(params)

    def scorm_zip(self):
        os.system('zip -r /tmp/scorm_dir.zip %s*')

    def scorm_import_folder(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(REMOTE_SCORM_SERVER, REMOTE_SCORM_PORT, REMOTE_SCORM_USER)

        scp = SCPClient(client.get_transport())

        os.makedirs(self.folder)
        scp.get(
            self.folder,
            self.folder,
            recursive=True
        )

        scp.close()
