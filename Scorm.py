import paramiko
import os
from scp import SCPClient
from config import *
from Command import Command
import random, string


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
        zip_name = self.scorm_zip()
        Command.command_execute(Command.activity_create_command(
            options=self.get_scorm_options(zip_name), type=self.type, id=self.course.id
        ))

    def get_scorm_options(self, name):
        params = []
        if self.section is not None:
            params.append('--section %s' % self.section)
        if self.title:
            params.append('--name "%s"' % self.title)

        params.append('--filepath /tmp/%s.zip' % name)

        return ' '.join(params)

    def scorm_zip(self):
        name = ''.join(random.choice(string.ascii_letters) for x in range(8))

        os.chdir(self.folder)
        os.system('zip -r /tmp/%s *' % name)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        return name

    def scorm_import_folder(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(REMOTE_SCORM_SERVER, REMOTE_SCORM_PORT, REMOTE_SCORM_USER)

        scp = SCPClient(client.get_transport())

        if not os.path.isdir('/opt/zope298/courses'):
            os.makedirs('/opt/zope298/courses')

        scp.get(
            self.folder,
            '/opt/zope298/courses/',
            recursive=True
        )

        scp.close()
