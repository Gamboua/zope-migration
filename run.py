#!/usr/bin/python

from Curso import Curso
import json
import sys

if len(sys.argv) != 2:
    print "Usage: %s <json_file>.json" % (sys.argv[0])
    sys.exit(1)

# Read json and parser to python dict array
with open(sys.argv[1], 'r') as f:
    j = json.loads(f.read())

for curso in j.get('cursos'):
    curso = Curso(curso)
    curso.add()