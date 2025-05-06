__all__ = ["session"]

class _Session(object):
    def __init__(self):
        self.token = None
        self.active_user = None
        self.login_email = None
        self.registration_name = None
        self._threads = []
    
    def new_thread(self, thread):
        self._threads.append(thread)
        return thread

    def delete_thread(self, thread):
        self._threads.remove(thread)


session = _Session()