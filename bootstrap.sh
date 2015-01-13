#!/bin/bash

PYTHON_VER_WANTED=2
DB_PATH=/vagrant/sql/schema.sql
DB_USER=hackit
DB_NAME=$DB_USER
DB_PASSWORD=$DB_USER
PIP_PATH=/vagrant/requirements.txt

# make sure we have the latest package DB
sudo apt-get update

if which python > /dev/null 2>&1;
then
	# if we have a non-python 2 install, we will need to manually intervene
	#  to correctly remove it - difficult to script it reliably
	# version check adapted from http://stackoverflow.com/a/6141633
	python_version="$(python -c "import sys; print(sys.version_info[0])")"
	if [ "$python_version" != "$PYTHON_VER_WANTED" ];
	then
		echo "DEBUG: No python$PYTHON_VER_WANTED installed, instead have v$python_version"
		echo "DEBUG: Will need intervention to reinstall with python$PYTHON_VER_WANTED."
		exit 1
	fi
else
	# ensure we have dev version - needed for psycopg2
	sudo apt-get install -y python-dev
fi

# and postgresql, https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-12-04
#  note we need the dev package "for building a server-side extension or libpq-dev for building a client-side application."
sudo apt-get install -y postgresql-server-dev-9.3 postgresql-contrib

>&2 echo "WARNING: This config is unsafe for production environments"

# create our db
sudo su - postgres -c "psql -c \"CREATE USER $DB_USER;\""
# for some reason we have to add this separately
sudo su - postgres -c "psql -c \"ALTER USER $DB_USER PASSWORD '$DB_PASSWORD';\""
sudo su - postgres -c "psql -c \"CREATE DATABASE $DB_NAME\";"
sudo su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;\""
# and import our schema
sudo su - postgres -c "psql -d $DB_NAME -f $DB_PATH"

# make sure we have pip (latest, due to http://stackoverflow.com/a/27425458)
# and any associated requirements globally
#  note we need this after postgresql
sudo easy_install -U pip
sudo pip install -r $PIP_PATH
