import json

from config import *
from Course import Course
from Scorm import Scorm

with open(JSON_FILE_PATH, 'r') as f:
    j = json.loads(f.read())

for curso in j.get('cursos'):
    curso = Course(curso)
