from config import *


class Command:

    def __init__(self):
        pass

    def course_create_command(self):
        return '%s course-config-set course %s format topics' % (MOOSH_COMMAND, self.curso_id)

    def activity_create_command(self):
        pass

    def command_execute(self):
        pass
