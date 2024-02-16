from decouple import config
from pathlib import Path
from django.utils.translation import gettext_lazy as _


# Base Settings
TIME_ZONE = config("TIME_ZONE", default='Asia/Tehran')

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = config('DEBUG', default=True, cast=bool)

# 'django-insecure-mj2_7hn=fi&%#7hg7r2p(k@lm%ugx_-s70bj#4$sbq7ywnr235'
SECRET_KEY = config("SECRET_KEY", default="development-secret-key") 

ALLOWED_HOSTS = \
    ['*'] if DEBUG else config(
            'ALLOWED_HOSTS',
            cast=lambda hosts: [h.strip() for h in hosts.split(",") if h]
        )


# Applications
EXTRA_APPS_prefix = [
    'jazzmin',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MY_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.items.apps.ItemsConfig",
    "apps.orders.apps.OrdersConfig",
    "apps.posts.apps.PostsConfig",
    "apps.sellers.apps.SellersConfig",
    "apps.users.apps.UsersConfig",
]

EXTRA_APPS_suffix = [
    'django_extensions',
    'rest_framework',
    'django_celery_beat',
    'ckeditor',
]

INSTALLED_APPS = EXTRA_APPS_prefix + DJANGO_APPS + MY_APPS + EXTRA_APPS_suffix

# Middleware's
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # */translation/*
    'django.middleware.locale.LocaleMiddleware',
    # */translation/*
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'apps.core.contexts.seller',
                'apps.core.contexts.category',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    # {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_TZ = True

# Translation
LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Persian')),
    # ('jp', _('Japanese')),
]

# Static & Media
STATIC_URL = 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User
AUTH_USER_MODEL = "users.User"

# Backends
AUTHENTICATION_BACKENDS = ("apps.users.backends.CustomModelBackend",)

# mode handling
if DEBUG:
    STATIC_ROOT = 'static'
    BASE_URL = "*"
    
    GRAPH_MODELS ={
        'all_applications': True,
        'graph_models': True,
    }
    
    # STATICFILES_DIRS = [
    #     BASE_DIR / 'static',
    # ]
    
    # Celery:    
    CELERY_BROKER_URL = config("CELERY_BROKER_URL_DEV")
    CELERY_TIMEZONE = TIME_ZONE

    # Cache
    # CACHES = {
    #     "default": {
    #         "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    #     }
    # }
    
    #____________________________________________________________
    REDIS_HOST = config("REDIS_HOST_dev")
    REDIS_PORT = config("REDIS_PORT_dev")
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    
    # Cache Services:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
    
    #____________________________________________________________
    
    # Email
    EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
    # EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT")
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
    # EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
    # DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
    
    # Development Sqlite3 db:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
else:
    STATIC_ROOT = BASE_DIR / 'static'
    
    REDIS_HOST = config("REDIS_HOST_pro")
    REDIS_PORT = config("REDIS_PORT_pro")
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    
    # Celery:
    CELERY_BROKER_URL = config("CELERY_BROKER_URL_PRO")
    CELERY_TIMEZONE = TIME_ZONE
    
    # Cache Services:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }
    
    # Email settings
    EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT")
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
    # EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
    # DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
    
    # Production postgresql db:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT"),
        },
    }
    
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Admin Panel",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "PK Center",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "PK Center",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "core/images/logo5.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "core/images/logo5.png",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": "core/images/logo5.png",

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "core/images/logo5.png",

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the PK Admin Panel",

    # Copyright on the footer
    "copyright": "PK Center",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string 
    "search_model": ["auth.User", "auth.Group"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},


        # external url that opens in a new window (Permissions can be added)
        {"name": "PK Github", "url": "https://github.com/pksenpai", "new_window": True},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Jazzmin Github", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "books"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Go to the Website", "url": "core:home", "new_window": True, "icon": "fa fa-home"},
        {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["auth", "books", "books.author", "books.book"],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages", 
            "url": "make_messages", 
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.Category": "fas fa-boxes",
        "core.Comment": "fas fa-comment-dots",
        "core.Report": "fa fa-ban",
        "items.Favorite": "fa fa-heart",
        "items.Item": "fa fa-cubes",
        "items.ItemImage": "fa fa-image",
        "items.Rating": "fa fa-star",
        "items.SellerItem": "fab fa-app-store-ios",
        "orders.Discount": "fas fa-qrcode",
        "orders.OrderItem": "fa fa-shopping-bag",
        "orders.Order": "fa fa-shopping-cart",
        "sellers.Seller": "fa fa-university",
        "users.Profile": "fas fa-user-circle",
        "users.User": "fas fa-user-alt",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": False,
}