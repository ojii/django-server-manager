from server_manager.settings import MOD_WSGI_FILES
from server_manager.backends.base import BaseBackend
from datetime import datetime
import os

class ModWSGIBackend(BaseBackend):
    def restart(self, site_id, request):
        filepath = MOD_WSGI_FILES.get(site_id)
        if filepath:
            try:
                os.utime(filepath, None)
                return True
            except IOError:
                return False
        return False

    def get_uptime(self, site_id, request):
        filepath = MOD_WSGI_FILES.get(site_id)
        if filepath:
            try:
                return datetime.fromtimestamp(os.stat(filepath)[-2])
            except IOError:
                return None
        return None
    
    def can_restart(self, site_id, request):
        filepath = MOD_WSGI_FILES.get(site_id)
        if filepath and os.path.exists(filepath):
            return True
        return False