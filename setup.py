from setuptools import setup, find_packages

version = __import__('server_manager').__version__

setup(
    name = 'django-server-manager',
    version = version,
    description = 'Django Server Manager',
    author = 'Jonas Obrist',
    url = 'http://github.com/ojii/django-server-manager',
    packages = find_packages(),
    zip_safe=False,
    package_data={
        'server_manager': [
            'templates/server_manager/*.html',
            'media/server_manager/js/*.js',
        ],
    },
)