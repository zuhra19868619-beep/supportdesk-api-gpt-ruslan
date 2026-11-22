import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.environ.get("SECRET_KEY","unsafe-local-dev-only")
DEBUG=os.environ.get("DEBUG","false").lower()=="true"\nif not DEBUG and SECRET_KEY=="unsafe-local-dev-only":\n raise RuntimeError("Set SECRET_KEY in production")
ALLOWED_HOSTS=os.environ.get("ALLOWED_HOSTS","localhost,127.0.0.1").split(",")
INSTALLED_APPS=["django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","rest_framework","django_filters","drf_spectacular","corsheaders","accounts","tickets"]
MIDDLEWARE=["django.middleware.security.SecurityMiddleware","whitenoise.middleware.WhiteNoiseMiddleware","corsheaders.middleware.CorsMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF="config.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="config.wsgi.application"
DATABASES={"default":dj_database_url.config(default=os.getenv("DATABASE_URL","sqlite:///"+str(BASE_DIR/"db.sqlite3")),conn_max_age=600,conn_health_checks=True)}
AUTH_PASSWORD_VALIDATORS=[{"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"}]
LANGUAGE_CODE="ru-ru"
TIME_ZONE="UTC"
USE_TZ=True
STATIC_URL="/static/"
STATIC_ROOT=BASE_DIR/"staticfiles"
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES":["rest_framework_simplejwt.authentication.JWTAuthentication"],"DEFAULT_PERMISSION_CLASSES":["rest_framework.permissions.IsAuthenticated"],"DEFAULT_FILTER_BACKENDS":["django_filters.rest_framework.DjangoFilterBackend","rest_framework.filters.SearchFilter","rest_framework.filters.OrderingFilter"],"DEFAULT_PAGINATION_CLASS":"rest_framework.pagination.PageNumberPagination","PAGE_SIZE":10,"DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema"}
SIMPLE_JWT={"ACCESS_TOKEN_LIFETIME":timedelta(minutes=30),"REFRESH_TOKEN_LIFETIME":timedelta(days=7)}
SPECTACULAR_SETTINGS={"TITLE":"SupportDesk API","VERSION":"1.0","DESCRIPTION":"WEPRO diploma"}
CORS_ALLOWED_ORIGINS=[x for x in os.environ.get("CORS_ALLOWED_ORIGINS","http://localhost:5173").split(",") if x]
SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO","https")\nSESSION_COOKIE_SECURE=not DEBUG\nCSRF_COOKIE_SECURE=not DEBUG\nSECURE_CONTENT_TYPE_NOSNIFF=True\nX_FRAME_OPTIONS="DENY"
