"""
    User class to simplify Firebase user record
"""
class User:
    """
        User class to simplify Firebase user record
    """
    DEFAULT_CLAIMS = {'UserType': 'User', 'AttackDefenseRole': 'NoTeam'}

    def __init__(self, user_record):
        self.user_record = user_record

    @property
    def uid(self):
        """
            Return user id
        """
        return self.user_record.uid

    @property
    def display_name(self):
        """
            Return user display name, or the string "None" if display_name is empty
        """
        display_name = self.user_record.display_name
        return "None" if display_name is None else display_name

    @property
    def email(self):
        """
            Return user email
        """
        return self.user_record.email

    @property
    def local_claims(self):
        """
            Get a dict with custom claims, and set unset claims to the values in DEFAULT_CLAIMS
        """
        custom_claims = self.user_record.custom_claims or {}
        claims = {}
        for claim, value in self.DEFAULT_CLAIMS.items():
            claims[claim] = custom_claims.get(claim, value)
        return claims
