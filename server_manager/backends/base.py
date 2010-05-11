class BaseBackend(object):    
    def restart(self, site_id, request):
        return False
        
    def start(self, site_id, request):
        return False
        
    def stop(self, site_id, request):
        return False

    def get_uptime(self, site_id, request):
        return None
        
    def can_restart(self, site_id, request):
        return False
        
    def can_start(self, site_id, request):
        return False
        
    def can_stop(self, site_id, request):
        return False