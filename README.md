![4|Linux](http://certificados.4linux.com.br/logo-top.png)
##Migração ZoDB p/ Moodle
### Moodle config
Para que a migração funcione, alguns parâmetros no moodle devem ser configurados antes.
#### Categorias
Dashboard > Site administration > Courses > Add a Category
- Parent: Top
- Category name: Unidades de negócio
- Category ID number: 3


- Parent: Top
- Category name: Gestão de conhecimento
- Category ID number: 9


- Parent: Top
- Category name: Unidades funcionais
- Category ID number: 6


- Parent: Top
- Category name: Liderança
- Category ID number: 5

### Cursos
Dashboard > Site administration > Courses > Course default settings
- Course format
  - Format: Topics format
  - Number of sections: 0

- Completion tracking
  - Completion tracking: Yes

### Scorm
Dashboard > Site administration > Plugins > Activity modules > Scorm Package
- Default display settings
    - Display courses structure on entry page: Yes
    - Display package: New window
    - Display activity name: False
    - Disable preview mode: Yes
    - Display course structure in player: Disabled
    - Display attempts status: No

### Questions
Dashboard > Site administration > Plugins > Activity modules > Quiz
- Automatically start a new page: After adding 10 questions
- Use a 'secure' popup window for attempts: Full screen pop-up with some Javascript security

### Repositório
Dashboard > Site administration > Plugins > Repositories > Manage repositories
- File system: enabled and visible
    - Settings 
        - Allow admins to add a file system...: checked
        - Create a repository instance
        - Name: scorm
        - Allow relative files: checked

Criar diretório dentro do moodledata
```
mkdir moodledata/repository/scorm -p
```
### Ambiente
Pacotes que devem ser garantidos
#### Pacotes e dependências
- Python 2.7 (apt-get)
  - libpq-dev
  - python-dev
  - libxslt-dev
  - libxml2-dev
  - libssl-dev
  - libffi-dev
- Python-pip (pip install)
  - psycopg2
  - lxml
  - cffi 1.8.2
  - cryptography 1.3.4
  - paramiko
  - scp
- Apache2
- PHP 5.6
  - php5-curl
  - php5-pgsql
  - php5-gd
  - php5-xmlrpc
  - php5-intl
- Postgres
  - Database com UTF8
- Composer
- Moosh


Copiar esses arquivos para dentro da pasta do moodle e do moosh
```
cp moosh/Moosh/Command/Moodle23/Course/CourseCreate.php /opt/moosh/Moosh/Command/Moodle23/
cp moosh/Moosh/Command/Moodle26/Activity/ActivityAdd.php /opt/moosh/Moosh/Command/Moodle26/
cp moosh/Moosh/Command/Moodle26/Question/QuestionImport.php /opt/moosh/Moosh/Command/Moodle26/Question/
cp moodle/lib/filestorage/file_storage.php /var/www/html/moodle/lib/filestorage/
cp moodle/mod/quiz/tests/generator/lib.php /var/www/html/moodle/mod/quiz/tests/generator/
cp moodle/mod/scorm/tests/generator/lib.php /var/www/html/moodle/mod/scorm/tests/generator/
```
### Configuração do script
Parâmetros no arquivo do config.py
#### MOODLE
- MOODLE_ROOT = Diretorio root do moodle
- MOODLE_SCORM_REPOSITORY = Diretório do repositório Scorm dentro do moodledata
- MOOSH_COMMAND = 'moosh -n -p %s' % MOODLE_ROOT

#### DATABASE
- BASE = Nome da base
- HOST = Host do banco
- USER = Usuário do Banco
- PASS = Senha da Base
- PORT = Porta postgresql

#### ENVIRONMENT
- JSON_FILE_PATH = json da migração
- QUESTIONS_XML = arquivo que será gerado pelo script de importação de questões

#### SCORM
- REMOTE_SCORM_SERVER = ip do servidor com pasta dos scorms
- REMOTE_SCORM_USER = usuario de acesso
- REMOTE_SCORM_PORT = porta de acesso

Validar o acesso ssh da máquina moodle com o servidor de diretórios scorm.
Fim
