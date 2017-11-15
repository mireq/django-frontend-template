===========================================================
Django frontend template with foundation 6
===========================================================

Install under ubuntu
--------------------

::

    sudo apt-get --yes install libjpeg-dev build-essential python-dev libfreetype6-dev git
    wget https://raw.github.com/mireq/django-frontend-template/master/install.sh&&chmod +x install.sh&&. ./install.sh

To run test server
------------------

::

    cd project
    make runserver

To enable autoprefixer (if not enabled automatically)
-----------------------------------------------------

::

    npm install postcss-cli autoprefixer

Then edit web/settings_local.py and add line:

::

    COMPRESS_POSTCSS_BINARY = '/path/to/postcss'
