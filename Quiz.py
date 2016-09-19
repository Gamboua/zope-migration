from Command import Command
from Import import import_questions
from DataBase import DataBase


class Quiz(DataBase):

    def __init__(self, json_dict, course):
        DataBase.__init__(self)

        self.course = course
        self.id = None
        self.questions = json_dict.get('questions')
        self.grading = json_dict.get('grading_scale')

        self.section = 0
        self.type = 'quiz'
        self.name = self.get_if_exists('title', json_dict)
        self.questionsperpage = 10
        self.showdesc = 1

    def quiz_add(self):
        self.id = Command.command_execute(Command.activity_create_command(
            options=self.get_quiz_options(), type=self.type, id=self.course.id
        ))
        self.id = self.id[0].rstrip()
        self.create_xml_file()
        Command.command_execute(Command.import_questions_command(
            self.id
        ))
        self.create_feedback()

    def create_feedback(self):
        success = self.grading[0].get('grade')
        failed = self.grading[1].get('grade')

        self.insert(
            'mdl_quiz_feedback',
            "quizid, feedbacktext, feedbacktextformat, mingrade, maxgrade",
            "'%s','%s','%s','%s','%s'" % (self.id, success, 1, 69.00000, 101.00000)
        )
        self.insert(
            'mdl_quiz_feedback',
            "quizid, feedbacktext, feedbacktextformat, mingrade, maxgrade",
            "'%s','%s','%s','%s','%s'" % (self.id, failed, 1, 0.00000, 69.00000)
        )

    def create_xml_file(self):
        import_questions(self.questions)

    def get_quiz_options(self):
        params = []
        if self.section is not None:
            params.append('--section %s' % self.section)
        if self.name:
            params.append('--name "%s"' % self.name)
        if self.questionsperpage:
            params.append('--pages %s' % self.questionsperpage)

        params.append('--showdesc %s' % self.showdesc)

        return ' '.join(params)

    def get_if_exists(self, parameter, json):
        return json.get(parameter) if parameter in json else None

