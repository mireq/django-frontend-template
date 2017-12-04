===========================================================
Django frontend template with foundation 6
===========================================================

Install under ubuntu
--------------------

::

    sudo apt-get --yes install libjpeg-dev build-essential python-dev libfreetype6-dev git
    wget https://raw.github.com/mireq/django-frontend-template/master/install.sh&&chmod +x install.sh&&. ./install.sh project_name

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

Sprites
-------

This project has builtin support for sprites with standard and @2x (retina)
resolution.

Sprites are compiled with command:

::

    make compilesprites

Source images are defined in web/assets.py in list named 'images':

::

    { 'name': 'check', 'src': 'img/sprites/check.png' },
    { 'name': 'radio', 'src': 'img/sprites/radio.png' },

Sprites are adressed using name attribute:

::

    /* file.scss */
    .icon-checkbox {
        @include sprite(check);
        display: block;
    }
