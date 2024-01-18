"""
    This module exports view functions for api calls related to managing labs
"""

from flask import request, g
from sagalabs.utils.validate import super_admin_required
from sagalabs.utils.backbone_client import BackboneClient

#API for labs:

@super_admin_required
def download_vpn():
    """
        Api endpoint for downloading ovpn config file
        Only allowed by super_admins
    """
    request_data = request.get_json()
    range_id = request_data.get('range')
    lab = request_data.get('lab')
    username = g.profile.email
    return BackboneClient().proxy_request(f'/api/vpn/{range_id}/{lab}/api/user/download',
                                          'post',
                                          request.cookies.get('sagalabs_auth'),
                                          {'username': username})

@super_admin_required
def stop_range():
    """
        Api endpoint for stopping a range
        Only allowed by super_admins
    """
    range_to_close = request.get_json().get('range')

    return BackboneClient().proxy_request(f'/api/azure/{range_to_close}/stop',
                                          'post',
                                          request.cookies.get('sagalabs_auth'))


@super_admin_required
def start_range():
    """
        Api endpoint for starting a range
        Only allowed by super_admins
    """
    range_to_start = request.get_json().get('range')

    return BackboneClient().proxy_request(f'/api/azure/{range_to_start}/start',
                                          'post',
                                          request.cookies.get('sagalabs_auth'))
