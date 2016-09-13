import subprocess
import psycopg2
import csv
from config import *
from Activity import Scorm, Quiz

class Curso:

    def __init__(self, curso_dict):
        self.db_host = DB_HOST
        self.db_user = DB_USER
        self.db_password = DB_PASSWORD
        self.db_name = DB_NAME
        self.db_port = DB_PORT

        self.moodle_path = MOODLE_PATH
        self.scorm_file_default_path = SCORM_FILE_DEFAULT_PATH
        self.moodle_cmd = 'moosh -n -p %s' % self.moodle_path

        self.curso_id = None
        self.title = curso_dict.get('title')
        self.description = curso_dict.get('description') if 'description' in curso_dict else None
        self.fullname = curso_dict.get('fullname') if 'fullname' in curso_dict else None
        self.activity = self.get_activity(curso_dict.get('activity')) if 'activity' in curso_dict else None
        self.tags = self.get_tags(
            activity=curso_dict.get('activity') if 'activity' in curso_dict else None,
            type=curso_dict.get('type') if 'type' in curso_dict else None
        )

        self.scorm = curso_dict.get('scorm') if 'scorm' in curso_dict else None
        self.quiz = curso_dict.get('quiz') if 'quiz' in curso_dict else None

    def add(self):
        # CREATE CURSO
        print 'adicionando curso %s' % self.title
        if not self.curso_exists():
            self.curso_id = self.command_execute(self.course_create_command())
        else:
            print '\tCurso ja existe'

        if self.curso_id:
            # FORMAT SECTION
            self.format_section()

            # CREATE ACTIVITY SCORM
            if self.scorm:
                scorm = Scorm(self)
                scorm.add()

            if self.quiz:
                quiz = Quiz(self)
                quiz.add()

    def curso_exists(self):
        return self.execute_query(
            "SELECT * FROM mdl_course WHERE fullname ILIKE '%s';" % self.title, True
        )

    def execute_query(self, sql, select=False):
        conn_str = "host=%s dbname=%s user=%s password=%s port=%s" % (
            self.db_host, self.db_name, self.db_user, self.db_password, self.db_port
        )
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

        return cursor.fetchone() if select else None

    def format_section(self):
        self.command_execute(self.course_format_command())

        self.execute_query("UPDATE mdl_course_format_options SET format='topics',value=0 WHERE courseid='%s' AND name='numsections';" % self.curso_id)

    def command_execute(self, command):
        output = subprocess.Popen(['' + command], stdout=subprocess.PIPE, shell=True).communicate()
        return output[0].replace('\n', '')

    def course_format_command(self):
        return '%s course-config-set course %s format topics' % (MOODLE_CMD, self.curso_id)

    def course_create_command(self):
        return "%s course-create %s" % (self.moodle_cmd, self.create_parameters())

    def create_parameters(self):
        params = ''

        if self.description:
            params = params + ' --description "%s"' % self.description
        if self.fullname:
            params = params + ' --fullname "%s"' % self.fullname
        if self.activity:
            params = params + ' --idnumber "%s"' % self.activity
            params = params + ' --category "%s"' % self.get_category()
        if self.tags:
            params = params + ' --tags \"%s\"' % self.tags

        params = params + ' "%s"' % self.title

        return params

    def get_activity(self, activity):
        if 'activity' in activity:
            activity = activity.get('activity').split('|')
            return activity[0][1:]

    def get_category(self):
        with open('categorias.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if self.activity == row['cod']:
                    category = self.execute_query(
                        "SELECT id FROM mdl_course_categories WHERE idnumber='%s';" % row['categoria'],
                        True
                    )
                    return category[0]

        return 1

    def get_tags(self, activity=None, type=None):
        list = []

        if 'knowledge_area' in activity:
            list.append(activity['knowledge_area'].split('|')[1])

        if 'concentration_area' in activity:
            list.append(activity['concentration_area'].split('|')[1])

        if 'modality' in activity:
            list.append(activity['modality'].split('|')[1])

        if type:
            list.append(type)

        return '|'.join(list)

