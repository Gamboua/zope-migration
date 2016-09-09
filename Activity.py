import subprocess
import os
import hashlib
import psycopg2
from config import *
from Import import import_questions
from copy_folders import create_folder


class Activity:

    def __init__(self):
        pass

    def command_execute(self, command):
        output = subprocess.Popen(['' + command], stdout=subprocess.PIPE, shell=True).communicate()
        return output[0].replace('\n', '')

    def activity_create_command(self, options):
        cmd = '%s activity-add %s %s %s' % (
            MOODLE_CMD, options, self.type, self.curso.curso_id
        )
        print cmd
        return cmd


class Quiz(Activity):

    def __init__(self, curso):
        Activity.__init__(self)
        self.curso = curso
        self.quiz_id = None
        self.section = 0
        self.type = 'quiz'
        self.xml_path = None
        self.name = self.curso.quiz.get('title')
        self.questionsperpage = 10
        self.showdesc = 1
        self.intro = self.get_intro()

    def add(self):
        if 'questions' in self.curso.quiz:
            self.quiz_id = self.command_execute(self.activity_create_command(
                options=self.create_parameters()
            ))
            self.create_xml_file()
            self.command_execute(self.import_questions_command())
            self.create_feedback(self.curso.quiz.get('grading_scale'))

    def create_parameters(self):
        params = []

        if self.section is not None:
            params.append('--section %s' % self.section)
        if self.name:
            params.append('--name "%s"' % self.name)
        if self.questionsperpage:
            params.append('--pages %s' % self.questionsperpage)
        # if self.intro:
        #     params.append("--intro '%s'" % self.intro)

        params.append('--showdesc %s' % self.showdesc)

        return ' '.join(params)

    def create_xml_file(self):
        import_questions(self.curso.quiz['questions'])

    def import_questions_command(self):
        return '%s question-import %s %s' % (
            MOODLE_CMD, JSON_DEFAULT_FILE, self.quiz_id
        )
        # return '%s question-import %s %s' % (
        #     MOODLE_CMD, 'test.xml', self.quiz_id
        # )

    def get_intro(self):
        return self.curso.quiz.get('directions')

    def execute_query(self, sql, select=False):
        conn_str = "host=%s dbname=%s user=%s password=%s port=%s" % (
            DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
        )
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

        return cursor.fetchone() if select else None

    def create_feedback(self, grade):
        success = grade[0].get('grade')
        failed  = grade[1].get('grade')

        self.execute_query(
            "INSERT INTO mdl_quiz_feedback(quizid,feedbacktext,feedbacktextformat,mingrade,maxgrade) VALUES('%s', '%s', '%s', '%s', '%s');" % (
                self.quiz_id, success, 1, 69.00000, 101.00000
            )
        )

        self.execute_query(
            "INSERT INTO mdl_quiz_feedback(quizid,feedbacktext,feedbacktextformat,mingrade,maxgrade) VALUES('%s', '%s', '%s', '%s', '%s');" % (
                self.quiz_id, failed, 1, 0.00000, 69.00000
            )
        )


class Scorm(Activity):

    def __init__(self, curso):
        Activity.__init__(self)
        self.curso = curso
        self.section = 0
        self.name = self.curso.scorm.get('title')
        self.type = 'scorm'

    def add(self):
        create_folder(self.curso.scorm.get('folder'))
        # copy scorm dir to moodle repository
        self.command_execute(self.activity_create_command(
            options=self.create_parameters('%simsmanifest.xml' % self.curso.scorm.get('folder')),
        ))

    def create_parameters(self, scorm_file):
        params = []

        if self.section is not None:
            params.append('--section %s' % self.section)
        if self.name:
            params.append('--name "%s"' % self.name)

        params.append('--filepath %s' % scorm_file)

        return ' '.join(params)