"""
Auxiliary tools
"""
from website.models import User

def collaborators_input_is_valid(string) -> tuple[list, bool]:
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



if __name__ == '__main__':
    l = []
    l2 = [True, False, False, True, True]
    print(evaluate_progress(l), evaluate_progress(l2))