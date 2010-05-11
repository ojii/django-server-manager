from django.db import models


class Server(models.Model):
    """
    We will use the permissions like this:
        server_manager.add_server: start server
        server_manager.change_server: restart server
        server_manager.delete_server: stop_server
    """