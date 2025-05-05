class Session:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance.user = None  # Add more attributes as needed
        return cls._instance

    def login(self, user_data):
        self.user = user_data

    def logout(self):
        self.user = None

    def is_authenticated(self):
        return self.user is not None