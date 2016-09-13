####
# DEV

DB_HOST = 'localhost'
DB_USER = 'postgres'
DB_PASSWORD = '123456'
DB_NAME = 'moodle31'
DB_PORT = 5432

MOODLE_PATH = '/var/www/html/moodle3.1/moodle'
SCORM_FILE_DEFAULT_PATH = '/var/www/html/moodle3.1/moodledata/repository/scorm/'

MOODLE_CMD = 'moosh -n -p %s'%(MOODLE_PATH)

JSON_DEFAULT_FILE = '/tmp/quiz.xml'

REMOTE_SSH_SERVER = '172.17.0.3'
REMOTE_SSH_USER = 'root'
# REMOTE_SSH_PASS = '132768'
# ssh-keygen
# ssh-copy-id root@endereco

####
# PROD

# DB_HOST = 'moodleead.ccjjwnnc8smp.us-east-1.rds.amazonaws.com'
# DB_USER = 'moodleead'
# DB_PASSWORD = '4Linux2015EAD'
# DB_NAME = 'moodleng'
# DB_PORT = 5432
#
# MOODLE_PATH = '/srv/www/moodleng'
# SCORM_FILE_DEFAULT_PATH = '/tmp/files/'
#
# MOODLE_CMD = 'moosh -n -p %s'%(MOODLE_PATH)
#
# JSON_DEFAULT_FILE = '/tmp/quiz.xml'
#
# REMOTE_SSH_SERVER = '172.17.0.2'
# REMOTE_SSH_USER = 'root'
# REMOTE_SSH_PASS = '132768'
