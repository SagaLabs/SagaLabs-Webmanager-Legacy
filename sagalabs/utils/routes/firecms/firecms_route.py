from flask import send_from_directory
import os
import logging
from sagalabs.utils.app import App

#logging.basicConfig(level=logging.DEBUG)

"""
def serve_firecms(app):
    @app.route('/firecms/', defaults={'path': 'index.html'})
    @app.route('/firecms/<path:path>')
    def serve_cms(path):
        firecms_build_path = os.path.join(app.root_path, 'firecms/dist')
        logging.debug(f"Trying to serve: {path} from {firecms_build_path}")

        if path != "" and os.path.exists(os.path.join(firecms_build_path, path)):
            logging.debug(f"Serving {path} from {firecms_build_path}")
            return send_from_directory(firecms_build_path, path)
        else:
            logging.debug(f"Serving index.html from {firecms_build_path}")
            return send_from_directory(firecms_build_path, 'index.html')

"""

def serve_cms(path):
    firecms_build_path = os.path.join(App.app().root_path, 'firecms/dist')
    logging.debug(f"Trying to serve: {path} from {firecms_build_path}")

    if path != "" and os.path.exists(os.path.join(firecms_build_path, path)):
        logging.debug(f"Serving {path} from {firecms_build_path}")
        return send_from_directory(firecms_build_path, path)
    else:
        logging.debug(f"Serving index.html from {firecms_build_path}")
        return send_from_directory(firecms_build_path, 'index.html')

def serve_cms_index():
    path = 'index.html'
    return serve_cms(path)