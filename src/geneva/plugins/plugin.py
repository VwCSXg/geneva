class Plugin():
    """
    Defines superclass for application plugins.
    """
    # Normal plugins evaluate strategies one by one for a clean slate.
    # Plugins can override that behavior and evaluate the entire population pool
    # at once with this flag.
    override_evaluation = False
