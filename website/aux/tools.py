"""
Auxiliary tools
"""
from ..models import User

def collaborators_input_is_valid(string):
    if not string:
        return [], True
    lst = [email.strip() for email in string.split(",")]
    collaborators = []
    for email in lst:
        user = User.query.filter_by(email=email).first()
        if not user:
            return [], False
        else:
            collaborators.append(user)
    else:
        return collaborators, True