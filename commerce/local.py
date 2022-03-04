from .settings import *
from .settings import INSTALLED_APPS, MIDDLEWARE, env

DEBUG = True

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    "localhost"
    # ...
]


if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]


CELERY_TASK_EAGER_PROPAGATES = True
