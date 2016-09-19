import subprocess
from config import *


class Command:

    def __init__(self):
        pass

    @staticmethod
    def course_create_command(options):
        return "%s course-create %s" % (
            MOOSH_COMMAND, options
        )

    @staticmethod
    def course_format_command(course):
        return '%s course-config-set course %s format topics' % (
            MOOSH_COMMAND, course.id
        )

    @staticmethod
    def activity_create_command(options, type, id):
        return '%s activity-add %s %s %s' % (
            MOOSH_COMMAND, options, type, id
        )

    @staticmethod
    def import_questions_command(id):
        return '%s question-import %s %s' % (
            MOOSH_COMMAND, QUESTIONS_XML, id
        )

    @staticmethod
    def command_execute(command):
        print command.encode('utf-8')
        return subprocess.Popen(['' + command.encode('utf-8')], stdout=subprocess.PIPE, shell=True).communicate()
