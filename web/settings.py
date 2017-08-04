import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = 'b8l@_l3c-=oqjpt=+!ew6!!qj0nog^)vr%ed=%eow!!9al#(mx'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'compressor',
	'design_utils',
]

MIDDLEWARE_CLASSES = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates'),],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
			'builtins': [
				'design_utils.templatetags.design_utils_tags',
				'compressor.templatetags.compress',
				'django.contrib.staticfiles.templatetags.staticfiles',
			]
		},
	},
]

WSGI_APPLICATION = 'web.wsgi.application'


DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}


AUTH_PASSWORD_VALIDATORS = [
	{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
	{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
	{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
	{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

COMPRESS_ENABLED = True

COMPRESS_PRECOMPILERS = (
	('text/x-scss', 'django_libsass.SassCompiler'),
)

COMPRESS_CSS_FILTERS = (
	'web.compress.PostcssFilter',
)

COMPRESS_POSTCSS_BINARY = 'postcss'
COMPRESS_POSTCSS_ARGS = '--use autoprefixer'

COMPRESS_REBUILD_TIMEOUT = 1

LIBSASS_SOURCEMAPS = True

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_generated', 'static')
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'compressor.finders.CompressorFinder',
)
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static_generated', 'media')
