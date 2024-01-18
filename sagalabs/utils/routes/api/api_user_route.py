"""
    This module exports view functions for api calls related to managing users
"""

from flask import request, abort, g, jsonify
from firebase_admin import auth

from sagalabs.utils.validate import login_required, dev_environment_required, super_admin_required
from sagalabs.utils.secrets import SELF_PROMOTE_KEY

@login_required
def promote_to_super_admin():
    """
        Api endpoint for promoting yourself to super_admin
        by inputing the self-promotion key.
    """
    #return request.get_json(), 200
    data = request.get_json()
    #key = data.get('promotion_key')

    if not 'promotion_key' in data:
        abort(400)
    if data['promotion_key'] == SELF_PROMOTE_KEY:
        claims = g.profile.local_claims
        claims["UserType"] = "SuperAdmin"
        auth.update_user(g.profile.uid, custom_claims=claims)
        return '', 200
    else:
        abort(401)

@super_admin_required
def update_custom_claim():
    """
        Api endpoint for updating custom claims
        Only allowed by super_admins
    """
    data = request.get_json()
    uid = data.get('uid')
    claim_name = data.get('claim_name')
    claim_value = data.get('claim_value')

    #Requst data validation
    if not claim_name in ['UserType', 'AttackDefenseRole']:
        abort(400)
    if claim_name == 'UserType' and not claim_value in ['User', 'Admin', 'SuperAdmin']:
        abort(400)
    if claim_name == 'AttackDefenseRole' and not claim_value in ['NoTeam', 'RedTeam', 'BlueTeam']:
        abort(400)

    user = auth.get_user(uid)
    custom_claims = user.custom_claims or {}
    custom_claims[claim_name] = claim_value
    auth.update_user(uid, custom_claims=custom_claims)
    return '', 200

# This DELETE api endpoint let's superadmins delete users by ID
@super_admin_required
def delete_user():
    """
        Api endpoint for deleting users
        Only allowed by super_admins
    """
    data = request.get_json()
    uid = data.get('uid')
    auth.delete_user(uid)
    return '', 200

@super_admin_required
@dev_environment_required
def get_all_data():
    """
        Api endpoint for retrieveing a json list of all users with custom claims
        Only allowed by super_admins
    """
    users = auth.list_users().iterate_all()
    user_data_list = []
    for user in users:
        user_data = {
            'uid': user.uid,
            'email': user.email,
            'custom_claims': user.custom_claims
        }
        user_data_list.append(user_data)

    return jsonify(user_data_list)
