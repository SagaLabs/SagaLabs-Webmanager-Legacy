"""
    This module exports function decorators, which are requirements 
    that must be met before the decorated function is called.

    This module also exports enforce_requirement. Usefull to create custom validate decorators
"""

from functools import wraps
from flask import g, redirect, url_for, abort
from sagalabs.utils.environment import environment

def enforce_requirement(validator, not_validated):
    """
        This function creates function wrappers, based on a (validator) that returns true or false.
        If validator returns true when called, the wrapped function is called.
        If validator returns false when called, not_validated is called
    """
    def x_required(wrapped_function):
        @wraps(wrapped_function)
        def decorated_function(*args, **kwargs):
            if validator():
                return wrapped_function(*args, **kwargs)
            return not_validated()
        return decorated_function
    return x_required

# This decorator redirects to sagalabs.login if not logged in
login_required = enforce_requirement(
    lambda: hasattr(g, 'profile_authorized'),
    lambda: redirect(url_for('sagalabs.login_redirect'))
)

# This decorator aborts with statuscode 403 (Forbidden) if user is not SuperAdmin
super_admin_required = enforce_requirement(
    lambda: hasattr(g, 'profile') and g.profile.local_claims["UserType"] == 'SuperAdmin',
    lambda: abort(403)
)
# This decorator aborts with statuscode 403 (Forbidden) if user is not SuperAdmin or Admin
admin_required = enforce_requirement(
    lambda: (hasattr(g, 'profile') and (g.profile.local_claims["UserType"] == 'SuperAdmin') or
    g.profile.local_claims["UserType"] == 'Admin'),
    lambda: abort(403)
)
# This decorator aborts with statuscode 403 (Forbidden) if branch is not development or local
dev_environment_required = enforce_requirement(
    lambda: environment.IS_ENVIRONMENT_DEV or environment.IS_ENVIRONMENT_LOCAL,
    lambda: abort(403)
)
