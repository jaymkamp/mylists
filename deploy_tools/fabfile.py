import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/jaymkamp/mylists.git'


# Automates deployment of current version of site with helper functions
def deploy():
	site_folder = f'/home/{env.user}/sites/{env.host}'
	run(f'mkdir -p {site_folder}')
	with cd(site_folder):
		_get_latest_source()
		_update_virtualenv()
		_create_or_update_dotenv()
		_update_static_files()
		_update_database()


# Does git clone if fresh deploy, or git fetch + reset of previous version
# already exists. 
def _get_latest_source():
	if exists('.git'):
		run('git fetch')
	else:
		run(f'git clone {REPO_URL} .')
	current_commit = local("git log -n 1 --format=%H", capture=True)
	run(f'git reset --hard {current_commit}')


# Checks if venv already exists, then updates the requirements
def _update_virtualenv():
	if not exists('virtualenv/bin/pip'):
		run(f'python3.6 -m venv virtualenv')
	run('./virtualenv/bin/pip install -r requirements.txt')


# Auto creates .env script, 
# adds certain env variables and creates secret_key if not present
def _create_or_update_dotenv():
	append('.env', 'DJANGO_DEBUG_FALSE=y')
	append('.env', f'SITENAME={env.host}')
	current_contents = run('cat .env')
	if 'DJANGO_SECRET_KEY' not in current_contents:
		new_secret = ''.join(random.SystemRandom().choices(
			'abcdefghijklmnopqrstuvwxyz0123456789', k=50
		))
		append('.env', f'DJANGO_SECRET_KEY={new_secret}')


def _update_static_files():
	# Uses venv version of py instead of system to get venv version of Django
	run('./virtualenv/bin/python manage.py collectstatic --noinput')





