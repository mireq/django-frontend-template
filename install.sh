#!/bin/bash

DUMPMAKE=
while true; do
	case "$1" in
		--dumpmake ) DUMPMAKE="$2"; shift 2 ;;
		-- ) shift; break ;;
		* ) break ;;
	esac
done

PROJECTNAME=$1
if [[ "$PROJECTNAME" == "" ]]
then
	PROJECTNAME='project'
fi

MAKEFILE=$DUMPMAKE
if [[ "$DUMPMAKE" == "" ]]
then
	MAKEFILE="$PROJECTNAME/Makefile"
fi

mkdir -p $PROJECTNAME

cat << 'EOF' > ${MAKEFILE}
.PHONY: all compilesprites migrate update update2 resetdb

EOF

echo "PROJECT=$PROJECTNAME" >> $MAKEFILE

cat << 'EOF' >> ${MAKEFILE}
PROJECT_SUBDIR=web

PYTHON=python3
VENV_PYTHON=venv/bin/python
DJANGO_MANAGE=cd ${PROJECT_SUBDIR}&&DJANGO_SETTINGS_MODULE=web.settings_local ../venv/bin/python manage.py

all: localinstall

.stamp_downloaded:
	git clone --recursive https://github.com/mireq/django-frontend-template.git ${PROJECT_SUBDIR}
	@touch .stamp_downloaded

.stamp_virtualenv: .stamp_downloaded
	wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py -O virtualenv.py
	${PYTHON} virtualenv.py venv --no-setuptools --no-pip --no-wheel -p ${PYTHON}
	rm virtualenv.py*
	@touch .stamp_virtualenv

.stamp_setuptools: .stamp_virtualenv
	wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py
	${VENV_PYTHON} get-pip.py
	rm get-pip.py*
	@touch .stamp_setuptools

.stamp_requirements: .stamp_setuptools
	venv/bin/pip install -r ${PROJECT_SUBDIR}/requirements.txt
	touch .stamp_requirements

.stamp_settings: .stamp_requirements
	cp ${PROJECT_SUBDIR}/web/settings_sample.py ${PROJECT_SUBDIR}/web/settings_local.py
	@touch .stamp_settings

compilesprites: .stamp_settings
	${DJANGO_MANAGE} compilesprites

migrate: .stamp_settings
	${DJANGO_MANAGE} migrate

compilemessages: .stamp_settings
	${DJANGO_MANAGE} compilemessages

runserver: .stamp_sampledata
	${DJANGO_MANAGE} runserver 0.0.0.0:8000

update: .stamp_settings
	cd ${PROJECT_SUBDIR}; git pull; git submodule sync --recursive
	@./${PROJECT_SUBDIR}/install.sh --dumpmake Makefile
	make update2

update2: .stamp_settings
	venv/bin/pip install -r ${PROJECT_SUBDIR}/requirements.txt
	${DJANGO_MANAGE} compilesprites
	${DJANGO_MANAGE} migrate
	#${DJANGO_MANAGE} compilemessages

.stamp_sampledata: .stamp_settings
	${DJANGO_MANAGE} compilesprites
	${DJANGO_MANAGE} migrate
	#${DJANGO_MANAGE} compilemessages
	#${DJANGO_MANAGE} loaddata forum/data/categories.json
	#${DJANGO_MANAGE} loaddata news/data/categories.json
	#${DJANGO_MANAGE} create_sample_data --verbosity 2
	#${DJANGO_MANAGE} loaddata wiki/data/pages.json
	#${DJANGO_MANAGE} rebuild_index --noinput
	@touch .stamp_sampledata

resetdb:
	rm -f ${PROJECT_SUBDIR}/db.sqlite3
	${DJANGO_MANAGE} migrate
	${DJANGO_MANAGE} loaddata forum/data/categories.json
	${DJANGO_MANAGE} create_sample_data
	${DJANGO_MANAGE} loaddata wiki/data/pages.json
	${DJANGO_MANAGE} rebuild_index --noinput

localinstall: .stamp_sampledata
	@echo "================================================"
	@echo "Installation successfull"
	@echo "For start enter: cd ${PROJECT}; make runserver"
	@echo "Open: http://127.0.0.1:8000 in browser"
	@echo "================================================"
EOF

if [[ "$DUMPMAKE" == "" ]]
then
	make -C $PROJECTNAME
fi
