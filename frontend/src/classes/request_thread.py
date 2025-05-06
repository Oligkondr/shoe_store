from PyQt5.QtCore import QThread, pyqtSignal
import requests

class RequestThread(QThread):
    finished = pyqtSignal(object, object) 

    def __init__(self, method, url, **kwargs):
        super().__init__()
        self._method = method
        self._url = url
        self._kwargs = kwargs 

    def run(self):
        try:
            response = requests.request(self._method, self._url, **self._kwargs)
            self.finished.emit(response, self)
        except Exception as e:
            self.finished.emit(e, self)