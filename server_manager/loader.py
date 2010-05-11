from server_manager.settings import SERVER_MANAGER_BACKENDS
from django.utils.importlib import import_module

def load_backend(name):
    mod, klass = name.rsplit('.', 1)
    module = import_module(mod)
    return getattr(module, klass)()


class BackendLoader(object):
    perms = {
        'start': 'server_manager.add_server',
        'can_start': 'server_manager.add_server',
        'stop': 'server_manager.delete_server',
        'can_stop': 'server_manager.delete_server',
        'restart': 'server_manager.change_server',
        'can_restart': 'server_manager.change_server',
    }
    
    def __init__(self):
        self.backends = []
        for backend in SERVER_MANAGER_BACKENDS:
            self.backends.append(load_backend(backend))

    def __getattr__(self, attr):
        def method(site_id, request, *args, **kwargs):
            # check permissions
            if attr in self.perms:
                if not request.user.has_perm(self.perms[attr]):
                    return False
            resp = False
            # iterate over backends until one returns a positive response
            for backend in self.backends:
                real = getattr(backend, attr)
                resp = real(site_id, request, *args, **kwargs)
                if resp:
                    return resp
            return resp
        return method
        
backend_loader = BackendLoader()