"""
    This module exports view functions for redirecting to another page
"""
from flask import redirect
from sagalabs.utils.environment import environment


def _redirect_backbone(page):
    return redirect(f'{environment.BACKBONE_URI}/{page}?redirect={environment.REDIRECT_URI}')

#Routes:
def login_redirect():
    """
        Redirect to login page
    """
    return _redirect_backbone('login')

def logout_redirect():
    """
        Redirect to logout page
    """
    return _redirect_backbone('logout')
