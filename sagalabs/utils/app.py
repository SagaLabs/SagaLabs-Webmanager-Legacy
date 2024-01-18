class App():
    """
        Makes the app created by Flask(__name__) available to import from the whole app.
        set(app) is called in __init__.py
    """
    _app = None

    @staticmethod
    def app():
        return App._app
    
    @staticmethod
    def set(app):
        App._app = app