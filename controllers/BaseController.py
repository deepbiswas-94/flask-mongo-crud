from flask import jsonify

class BaseController:
    prepareResponse = lambda *args, **kwargs: (jsonify(args[0]), 200)