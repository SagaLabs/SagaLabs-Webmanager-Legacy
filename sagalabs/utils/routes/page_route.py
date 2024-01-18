"""
    This module exports view functions for showing pages to users
"""
import json

from flask import render_template, request
from firebase_admin import auth

from sagalabs.utils.backbone_client import BackboneClient
from sagalabs.utils.data_structure.user import User
from sagalabs.utils.data_structure.range import Range
from sagalabs.utils.data_structure.lab import Lab
from sagalabs.utils.validate import login_required, super_admin_required

def home():
    """
        Displays home page
    """
    return render_template('page/index/index.html')

@login_required
@super_admin_required
def labs_page():
    """
        Page for displaying and managing labs
    """
    use_sample_data = False

    backbone_client = BackboneClient()
    if use_sample_data:
        with open(
            'sagalabs/static/sampleForTestRanges.json',
            'r', 
            encoding="utf-8"
            ) as sample_range:

            ranges = json.load(sample_range)

        with open(
            'sagalabs/static/sampleForTestRangesState.json',
            'r',
            encoding="utf-8"
            ) as sample_state:

            power_state = json.load(sample_state)
    else:
        ranges = backbone_client.proxy_request(
            '/api/azure/ranges',
            'get', 
            request.cookies.get('sagalabs_auth')
        ).json

        power_state = backbone_client.proxy_request('/api/azure/getServers/powerState',
                                                    'get',
                                                    request.cookies.get('sagalabs_auth')).json

    def range_builder():
        range_objects = []
        for range_name, range_value in ranges.items():
            labs_in_range = []
            for lab_name, lab_value in range_value.items():
                lab_state_json = power_state.get(range_name, {}).get(lab_name, {})
                labs_in_range.append(Lab(lab_name, lab_value, lab_state_json))
            range_objects.append(Range(range_name, labs_in_range))
        return range_objects

    return render_template('page/labs/labs.html', ranges=range_builder())

@login_required
def users_page():
    """
        Page for displaying and managing users
    """
    # Get a list of users from firebase auth
    user_record_list = auth.list_users().users
    # Creates a user object from user_record_list
    users = list(map(User, user_record_list))
    #Sorts users based on primarily username and secondaryly email
    sorted_users = sorted(users, key=lambda user: user.display_name + user.email)
    return render_template('page/users/users.html', users=sorted_users)
