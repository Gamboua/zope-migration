####
# MOODLE CONFIGURATION
MOODLE_ROOT = '/var/www/html/moodle3.1/moodle/'
MOODLE_SCORM_REPOSITORY = '/var/www/html/moodle3.1/moodledata/repository/scorm/'
MOOSH_COMMAND = 'moosh -n -p %s' % MOODLE_ROOT

####
# DATABASE CONFIGURATION
BASE = 'moodle31'
HOST = 'localhost'
USER = 'postgres'
PASS = '123456'
PORT = '5432'

####
# ENVIRONMENT
JSON_FILE_PATH = 'with_questions.json'
QUESTIONS_XML = '/tmp/quiz.xml'

####
# SCORM SERVER
REMOTE_SCORM_SERVER = '172.17.0.3'
REMOTE_SCORM_USER = 'root'