from django.conf import settings

__all__ = ['SERVER_MANAGER_BACKENDS', 'MOD_WSGI_FILES']

def patch():
    for key in globals().keys():
        if key in __all__:
            confvalue = getattr(settings, key, None)
            if confvalue is not None:
                globals()[key] = confvalue
        
SERVER_MANAGER_BACKENDS = ['server_manager.backends.base.BaseBackend']
MOD_WSGI_FILES = {
    # SITE_ID: PATH_TO_FILE,
}

patch()