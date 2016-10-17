####
# MOODLE CONFIGURATION
MOODLE_ROOT = '/var/www/html/moodle3.1/moodle/'
MOODLE_SCORM_REPOSITORY = '/var/www/html/moodle3.1/moodledata/repository/scorm/'
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
JSON_FILE_PATH = 'one_course.json'
QUESTIONS_XML = '/tmp/quiz.xml'

####
# SCORM SERVER
REMOTE_SCORM_SERVER = 'scormserver'
REMOTE_SCORM_USER = 'scormserveruser'
REMOTE_SCORM_PORT = 22
