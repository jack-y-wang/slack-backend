from datetime import datetime
from flask import jsonify
  
import abc

class BaseController:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_path(self):  # URI-path that begins and ends with a '/'
        return ""

    @abc.abstractmethod
    def get_methods(self):  # List of different HTTP methods supported
        return []

    @abc.abstractmethod
    def response(self, **kwargs):
        return None

class Controller(BaseController):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def content(self, **kwargs):
        return dict()

    def get_name(self):
        return self.get_path().replace("/", "-")

    def response(self, **kwargs):
        try:
            content = self.content(**kwargs)
            return jsonify({"success": True, "data": content, "timestamp": round(datetime.now().timestamp())})
        except Exception as e:
            return jsonify(
                {"success": False, "data": {"errors": [str(e)]}, "timestamp": round(datetime.now().timestamp())}
            )
            