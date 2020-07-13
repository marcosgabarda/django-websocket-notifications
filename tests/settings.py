from django.utils.translation import gettext_lazy as _

DEBUG = True
USE_TZ = True

SECRET_KEY = "dummy"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

INSTALLED_APPS = [
    "django.forms",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "websocket_notifications",
    "tests.app.apps.TestAppConfig",
]

ROOT_URLCONF = "tests.urls"
SITE_ID = 1
USE_I18N = True
LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English")]
LOCALE_PATHS = ["./websocket_notifications/locale/"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "debug": DEBUG,
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]
STATIC_URL = "/static/"
WSGI_APPLICATION = "tests.wsgi.application"

# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
# See: http://www.django-rest-framework.org/
INSTALLED_APPS += ("rest_framework", "rest_framework.authtoken")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    )
}
