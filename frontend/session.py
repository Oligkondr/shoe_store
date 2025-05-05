__all__ = ["session"]

class _Session(object):
    def __init__(self):
        self.active_user = None
        self.login_email = None
        self.registration_name = None


session = _Session()