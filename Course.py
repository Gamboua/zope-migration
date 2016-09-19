import csv
from Command import Command
from DataBase import DataBase


class Course(DataBase):

    def __init__(self, json_dict):
        DataBase.__init__(self)

        self.id = None
        self.type = self.get_if_exists('type', json_dict)
        self.description = self.get_if_exists('description', json_dict)
        self.title = self.get_if_exists('title', json_dict)

        self.activity = self.get_if_exists('activity', json_dict)
        self.activity_number = self.get_activity_number() if self.activity else None
        self.category_number = self.get_category_number() if self.activity else None
        self.tags = self.get_tags()

    def course_add(self):
        self.course_prepare()
        self.id = self.course_create()
        self.id = self.id[0].rstrip()

    def course_create(self):
        return Command.command_execute(Command.course_create_command(
            self.get_course_options()
        ))

    def get_course_options(self):
        params = []
        if self.description:
            params.append('--description "%s"' % self.description)
        if self.activity_number:
            params.append('--idnumber "%s"' % self.activity_number)
        if self.category_number:
            params.append('--category "%s"' % self.category_number)
        if self.tags:
            params.append('--tags "%s"' % self.tags)

        params.append('"%s"' % self.title)

        return ' '.join(params)

    def get_tags(self):
        list = []
        if 'knowledge_area' in self.activity:
            list.append(self.activity['knowledge_area'].split('|')[1])

        if 'concentration_area' in self.activity:
            list.append(self.activity['concentration_area'].split('|')[1])

        if 'modality' in self.activity:
            list.append(self.activity['modality'].split('|')[1])

        if self.type:
            list.append(self.type)

        return '|'.join(list)

    def get_activity_number(self):
        activity = self.activity.get('activity').split('|')
        return activity[0]

    def get_category_number(self):
        with open('categorias.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if self.activity_number[1:] == row['cod']:
                    category = self.fetch(
                        table='mdl_course_categories',
                        where="idnumber='%s'" % row['categoria'],
                        columns='id'
                    )
                    return category[0]
        return 1

    def get_if_exists(self, parameter, json):
        return json.get(parameter) if parameter in json else None

    def course_prepare(self):
        # check if course exists
        self.course_exists()

    def course_format_section(self):
        Command.command_execute(Command.course_format_command(self))

        params = ["format='topics'", "value=0"]
        self.update(
            'mdl_course_format_options',
            ', '.join([str(i) for i in params]),
            "courseid='%s' AND name = 'numsections'" % self.id
        )

    def course_exists(self):
        course = self.fetch('mdl_course', "fullname ILIKE '%s'" % self.title, True)

        if course:
            raise Exception('Curso ja existe')
