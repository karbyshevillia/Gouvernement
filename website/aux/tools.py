"""
Auxiliary tools
"""
from website.models import User, Task, Task
import re
import datetime

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

def project_search(search_input: str, projects_list):

    SEARCH_ATTRIBUTES = [
        "title_contains",
        "priority",
        "description_contains",
        "supervisor_email",
        "supervisor_first_name",
        "creation_date_start",
        "creation_date_end",
        "deadline_start",
        "deadline_end",
        "are_collaborators",
        "status",
        "progress_start",
        "progress_end"
    ]

    ATTR_REGEX = r"\b(?P<ATTR_NAME>\w*)=<(?P<ATTR_VALUE>[^>]*)>"

    searched_attributes_dict = dict(re.findall(ATTR_REGEX, search_input))

    if not searched_attributes_dict:
        return projects_list

    for key, value in searched_attributes_dict.items():

        if key not in SEARCH_ATTRIBUTES:
            pass
        elif key == "title_contains":
            projects_list = projects_list.filter(Task.title.contains(value))
        elif key == "priority":
            projects_list = projects_list.filter(Task.priority == int(value))
        elif key == "description_contains":
            projects_list = projects_list.filter(Task.description.contains(value))
        elif key == "supervisor_email":
            projects_list = projects_list.filter(Task.supervisor_user.has(email = value))
        elif key == "supervisor_first_name":
            projects_list = projects_list.filter(Task.supervisor_user.has(first_name = value))
        elif key == "creation_date_start":
            projects_list = projects_list.filter(Task.creation_date >= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "creation_date_end":
            projects_list = projects_list.filter(Task.creation_date <= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "deadline_start":
            projects_list = projects_list.filter(Task.deadline >= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "deadline_end":
            projects_list = projects_list.filter(Task.deadline <= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "are_collaborators":
            value_list = collaborators_input_is_valid(value)[0]
            for email in value_list:
                projects_list = projects_list.filter(Task.current_collaborators.any(email=email))
        elif key == "status":
            boolean_status = (value == "OPEN")
            projects_list = projects_list.filter(Task.status == boolean_status)
        elif key == "progress_start":
            projects_list = projects_list.filter(Task.progress >= int(value))
        elif key == "progress_end":
            projects_list = projects_list.filter(Task.progress <= int(value))

    return projects_list


def task_search(search_input: str, tasks_list):

    SEARCH_ATTRIBUTES = [
        "title_contains",
        "priority",
        "description_contains",
        "assigner_email",
        "assigner_first_name",
        "creation_date_start",
        "creation_date_end",
        "deadline_start",
        "deadline_end",
        "are_assignees",
        "status"
    ]

    ATTR_REGEX = r"\b(?P<ATTR_NAME>\w*)=<(?P<ATTR_VALUE>[^>]*)>"

    searched_attributes_dict = dict(re.findall(ATTR_REGEX, search_input))

    if not searched_attributes_dict:
        return tasks_list

    for key, value in searched_attributes_dict.items():

        if key not in SEARCH_ATTRIBUTES:
            pass
        elif key == "title_contains":
            tasks_list = tasks_list.filter(Task.title.contains(value))
        elif key == "priority":
            tasks_list = tasks_list.filter(Task.priority == int(value))
        elif key == "description_contains":
            tasks_list = tasks_list.filter(Task.description.contains(value))
        elif key == "supervisor_email":
            tasks_list = tasks_list.filter(Task.assigned_by_user.has(email = value))
        elif key == "supervisor_first_name":
            tasks_list = tasks_list.filter(Task.assigned_by_user.has(first_name = value))
        elif key == "creation_date_start":
            tasks_list = tasks_list.filter(Task.creation_date >= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "creation_date_end":
            tasks_list = tasks_list.filter(Task.creation_date <= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "deadline_start":
            tasks_list = tasks_list.filter(Task.deadline >= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "deadline_end":
            tasks_list = tasks_list.filter(Task.deadline <= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "are_collaborators":
            value_list = collaborators_input_is_valid(value)[0]
            for email in value_list:
                tasks_list = tasks_list.filter(Task.current_assignees.any(email=email))
        elif key == "status":
            boolean_status = (value == "OPEN")
            tasks_list = tasks_list.filter(Task.status == boolean_status)

    return tasks_list
# if __name__ == '__main__':
#     # test = "title_contains=<title>, priority=<1>"
#     # print(project_search(test))