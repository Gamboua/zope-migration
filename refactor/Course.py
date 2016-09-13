from Command import Command
from DataBase import DataBase


class Course(Command, DataBase):

    def __init__(self, json_dict):
        self.type = self.get_if_exists('type', json_dict)
        self.description = self.get_if_exists('description', json_dict)
        self.title = self.get_if_exists('title', json_dict)

    def get_if_exists(self, parameter, json):
        return json.get(parameter) if parameter in json else None

    def course_prepare(self):
        # check if course exists
        self.course_exists()

    def course_create(self):
        pass

    def course_format_section(self):
        pass

    def course_exists(self):
        pass