"""
    Initialization of flask
"""
from flask import Flask
from sagalabs import sagalabs
from sagalabs.utils.app import App
#from sagalabs.utils.routes.firecms.firecms_route import serve_firecms  # Adjust import based on where you put firecms_route.py

def create_app():
    """
        This function is called when flask is run with command
    """
    # create and configure the app
    app = Flask(__name__)
    App.set(app)
    app.register_blueprint(sagalabs.bp)

    #serve_firecms(app) #todo: find a better way to serve meaby?
    #Print all routes with endpoint, method and path.
    #for rule in app.url_map.iter_rules():
    #   print(f"Endpoint: {rule.endpoint}, Methods: {', '.join(rule.methods)}, Path: {rule.rule}")

    return app
