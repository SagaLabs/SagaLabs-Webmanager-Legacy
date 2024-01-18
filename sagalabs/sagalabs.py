"""Creates blueprint for flask application"""
import json
import datetime

from flask import Blueprint, request, g
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

from sagalabs.utils.data_structure.user import User
from sagalabs.utils.backbone_client import BackboneClient
from sagalabs.utils.environment import environment
from sagalabs.utils.secrets import FIREBASE_SERVICE_ACCOUNT_JSON

from sagalabs.utils.routes import page_route, redirect_route
from sagalabs.utils.routes.api import api_labs_route, api_user_route
from sagalabs.utils.routes.firecms import firecms_route

# For keeping track of time since initialization
start_time = datetime.datetime.now()

# Initialize Firebase with Service Account
cred_dict = json.loads(FIREBASE_SERVICE_ACCOUNT_JSON)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

# Initialize blueprint
bp = Blueprint('sagalabs', __name__, url_prefix='')

# Backbone Client
backboneClient = BackboneClient()

# This function runs before a request
# This extract user data from cookie and appends it under the global variable 'g'
@bp.before_request
def validate_cookie():
    """ 
        This function runs before a request
        This extract user data from cookie and appends it under the global variable 'g'
    """
    cookie = request.cookies.get('sagalabs_auth')
    if cookie:
        profile = auth.verify_session_cookie(cookie, check_revoked=True)
        user_record = auth.get_user(profile["user_id"])
        user = User(user_record)
        g.profile = user
        g.profile_authorized = True

# This function runs before template render
# This sets variables to be used by every template
@bp.context_processor
def inject_value():
    """
        This function runs before template render
        This sets variables to be used by every template
    """
    template_variables = {}

    time_since_restart = datetime.datetime.now() - start_time
    time_format_object = {
        'days': time_since_restart.days,
        'hours': time_since_restart.seconds // 3600,
        'minutes': (time_since_restart.seconds % 3600) // 60
    }
    template_variables["run_stamp"] = time_format_object
    template_variables["environment"] = environment.ENVIRONMENT
    template_variables["is_environment_development"] = environment.IS_ENVIRONMENT_DEV or environment.IS_ENVIRONMENT_LOCAL
    if hasattr(g, "profile_authorized"):
        template_variables["profile_authorized"] = g.profile_authorized
        template_variables["profile"] = g.profile
    return template_variables

def build_routes(routes):
    """
        This function builds routes from a dict. 
        Routes are build recursively with respect to their path.
        An exception is top level "page", which routes gets unpacked at top level "/".
        If no method is provided, it defaults to 'GET'
    """

    def build_route(path, function, methods):
        bp.add_url_rule(path, view_func=function, methods=methods)

    def build_recursively(route_dict, sub_dir):
        for key, value in route_dict.items():
            path = f'{sub_dir}/{key}'

            if isinstance(value, dict):
                build_recursively(value, path)
            elif isinstance(value, list):
                build_route(path, value[0], [value[1]])
            else:
                build_route(path, value, ['GET'])

   #Routes are unpacked based on their parrent, except "page" which is unpacked at top level
    for key, value in routes.items():
        if key == 'page':
            build_recursively(value, '/')
        else:
            build_recursively(value, f'/{key}')

build_routes({
    'page':{
        '/': page_route.home,
        "labs": page_route.labs_page,
        "users": page_route.users_page
    },
    'redirect':{
        'login': redirect_route.login_redirect,
        'logout': redirect_route.logout_redirect
    },
    'api':{
        'labs': {
            'start_range': [api_labs_route.start_range, 'PUT'],
            'stop_range': [api_labs_route.stop_range, 'PUT'],
            'download_vpn': [api_labs_route.download_vpn, 'POST']
        },
        'user':{
            'get_all_data': [api_user_route.get_all_data, 'GET'],
            'promote_self': [api_user_route.promote_to_super_admin, 'PUT'],
            'update_claim': [api_user_route.update_custom_claim, 'PUT'],
            'delete': [api_user_route.delete_user, 'DELETE']
        }
    },
    'firecms':{
        '/': firecms_route.serve_cms_index,
        '<path:path>': firecms_route.serve_cms
    }
})
