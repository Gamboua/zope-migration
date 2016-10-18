####
# MOODLE CONFIGURATION
MOODLE_ROOT = '/var/www/html/moodle/'
MOODLE_SCORM_REPOSITORY = '/var/www/html/moodledata/repository/scorm/'
MOOSH_COMMAND = 'moosh -n -p %s' % MOODLE_ROOT

####
# DATABASE CONFIGURATION
BASE = 'basename'
HOST = 'localhost'
USER = 'baseuser'
PASS = 'basepass'
PORT = 5432

####
# ENVIRONMENT
JSON_FILE_PATH = 'full_courses.json'
QUESTIONS_XML = '/tmp/quiz.xml'

####
# SCORM SERVER
REMOTE_SCORM_SERVER = 'scormserver'
REMOTE_SCORM_USER = 'scormserveruser'
REMOTE_SCORM_PORT = 22
