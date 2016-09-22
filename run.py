import json

from config import *
from Course import Course
from Scorm import Scorm
from Quiz import Quiz

with open(JSON_FILE_PATH, 'r') as f:
    j = json.loads(f.read())

for item in j.get('cursos'):
    try:
        course = Course(item)
        course.course_add()
        course.course_format_section()

        if 'scorm' in item:
            scorm = Scorm(item.get('scorm'), course)
            scorm.scorm_add()
        if 'quiz' in item:
            quiz = Quiz(item.get('quiz'), course)
            quiz.quiz_add()
    except Exception as e:
        print e
