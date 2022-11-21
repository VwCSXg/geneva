import os

BASEPATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASEPATH)


class Plugin():
    """
    Defines superclass for application plugins.
    """
    # Normal plugins evaluate strategies one by one for a clean slate.
    # Plugins can override that behavior and evaluate the entire population pool
    # at once with this flag.
    override_evaluation = False
