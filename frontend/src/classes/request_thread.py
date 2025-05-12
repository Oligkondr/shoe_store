from PyQt5.QtCore import QThread, pyqtSignal
import requests
import traceback


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
            traceback.print_exc()
            self.finished.emit(e, self)
