__all__ = ["session"]

class _Session(object):
    def __init__(self):
        self.token = None
        self.active_user = None

        self.login_email = None
        self.registration_name = None
        
        self.curr_window = None

        # Хранение асинхронных запросов
        self.threads = []
        
        # Хранение окон, которые необходимо закрыть при закрытии главного
        self.windows = []

session = _Session()