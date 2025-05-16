"""
Auxiliary tools
"""

from website.models import User, Project, Task
import re
import datetime
from sqlalchemy.sql import desc, or_

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
        "are_supervisors_or",
        "supervisor_email",
        "supervisor_first_name",
        "creation_date_start",
        "creation_date_end",
        "deadline_start",
        "deadline_end",
        "are_collaborators_or",
        "are_collaborators_and",
        "status",
        "progress_start",
        "progress_end",
        "priority_sort",
        "creation_date_sort",
        "deadline_sort",
        "status_sort",
        "progress_sort"
    ]

    PRIORITY_PERMITTED = [str(i) for i in range(1, 6)]

    STATUS_PERMITTED = ["OPEN",
                        "CLOSED"]

    STATUS_SORT_PERMITTED = ["OPEN_FIRST",
                             "CLOSED_FIRST"]

    SORT_PERMITTED = ["ASC",
                      "DESC"]


    ATTR_REGEX = r"\b(?P<ATTR_NAME>\w*)=<(?P<ATTR_VALUE>[^>]*)>"

    searched_attributes_dict = dict(re.findall(ATTR_REGEX, search_input))

    if not searched_attributes_dict:
        return projects_list

    for key, value in searched_attributes_dict.items():

        if key not in SEARCH_ATTRIBUTES:
            continue
        elif key == "title_contains":
            projects_list = projects_list.filter(Project.title.contains(value))
        elif key == "priority":
            if value not in PRIORITY_PERMITTED:
                continue
            projects_list = projects_list.filter(Project.priority == int(value))
        elif key == "description_contains":
            projects_list = projects_list.filter(Project.description.contains(value))
        elif key == "are_supervisors_or":
            if not collaborators_input_is_valid(value)[1]:
                continue
            value_list = collaborators_input_is_valid(value)[0]
            projects_list = projects_list.filter(
                or_(*[Project.supervisor == user.id for user in value_list])
            )
        elif key == "supervisor_email":
            projects_list = projects_list.filter(Project.supervisor_user.has(email = value))
        elif key == "supervisor_first_name":
            projects_list = projects_list.filter(Project.supervisor_user.has(first_name = value))
        elif key == "creation_date_start":
            projects_list = projects_list.filter(Project.creation_date >= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "creation_date_end":
            projects_list = projects_list.filter(Project.creation_date <= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "deadline_start":
            projects_list = projects_list.filter(Project.deadline >= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "deadline_end":
            projects_list = projects_list.filter(Project.deadline <= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "are_collaborators_or":
            if not collaborators_input_is_valid(value)[1]:
                continue
            value_list = collaborators_input_is_valid(value)[0]
            projects_list = projects_list.filter(
                or_(*[Project.current_collaborators.any(User.id == user.id) for user in value_list])
            )
        elif key == "are_collaborators_and":
            if not collaborators_input_is_valid(value)[1]:
                continue
            value_list = collaborators_input_is_valid(value)[0]
            for user in value_list:
                projects_list = projects_list.filter(Project.current_collaborators.any(User.id == user.id))
        elif key == "status":
            if value not in STATUS_PERMITTED:
                continue
            boolean_status = (value == "OPEN")
            projects_list = projects_list.filter(Project.status == boolean_status)
        elif key == "progress_start":
            projects_list = projects_list.filter(Project.progress >= int(value))
        elif key == "progress_end":
            projects_list = projects_list.filter(Project.progress <= int(value))
        elif key == "priority_sort":
            if value not in SORT_PERMITTED:
                continue
            elif value == "ASC":
                projects_list = projects_list.order_by(Project.priority)
            elif value == "DESC":
                projects_list = projects_list.order_by(desc(Project.priority))
        elif key == "creation_date_sort":
            if value not in SORT_PERMITTED:
                continue
            elif value == "ASC":
                projects_list = projects_list.order_by(Project.creation_date)
            elif value == "DESC":
                projects_list = projects_list.order_by(desc(Project.creation_date))
        elif key == "deadline_sort":
            if value not in SORT_PERMITTED:
                continue
            elif value == "ASC":
                projects_list = projects_list.order_by(Project.deadline)
            elif value == "DESC":
                projects_list = projects_list.order_by(desc(Project.deadline))
        elif key == "status_sort":
            if value not in STATUS_SORT_PERMITTED:
                continue
            elif value == "OPEN_FIRST":
                projects_list = projects_list.order_by(desc(Project.status))
            elif value == "CLOSED_FIRST":
                projects_list = projects_list.order_by(Project.status)
        elif key == "progress_sort":
            if value not in SORT_PERMITTED:
                continue
            elif value == "ASC":
                projects_list = projects_list.order_by(Project.progress)
            elif value == "DESC":
                projects_list = projects_list.order_by(desc(Project.progress))

    return projects_list


def task_search(search_input: str, tasks_list):

    SEARCH_ATTRIBUTES = [
        "title_contains",
        "priority",
        "description_contains",
        "are_assigners_or",
        "assigner_email",
        "assigner_first_name",
        "creation_date_start",
        "creation_date_end",
        "deadline_start",
        "deadline_end",
        "are_assignees_or",
        "are_assignees_and",
        "status",
        "priority_sort",
        "creation_date_sort",
        "deadline_sort",
        "status_sort"
    ]

    PRIORITY_PERMITTED = [str(i) for i in range(1, 6)]

    STATUS_PERMITTED = ["OPEN",
                        "CLOSED"]

    STATUS_SORT_PERMITTED = ["OPEN_FIRST",
                             "CLOSED_FIRST"]

    SORT_PERMITTED = ["ASC",
                      "DESC"]

    ATTR_REGEX = r"\b(?P<ATTR_NAME>\w*)=<(?P<ATTR_VALUE>[^>]*)>"

    searched_attributes_dict = dict(re.findall(ATTR_REGEX, search_input))

    if not searched_attributes_dict:
        return tasks_list

    for key, value in searched_attributes_dict.items():

        if key not in SEARCH_ATTRIBUTES:
            continue
        elif key == "title_contains":
            tasks_list = tasks_list.filter(Task.title.contains(value))
        elif key == "priority":
            tasks_list = tasks_list.filter(Task.priority == int(value))
        elif key == "description_contains":
            tasks_list = tasks_list.filter(Task.description.contains(value))
        elif key == "are_assigners_or":
            if not collaborators_input_is_valid(value)[1]:
                continue
            value_list = collaborators_input_is_valid(value)[0]
            tasks_list = tasks_list.filter(
                or_(*[Task.assigner == user.id for user in value_list])
            )
        elif key == "assigner_email":
            tasks_list = tasks_list.filter(Task.assigned_by_user.has(email = value))
        elif key == "assigner_first_name":
            tasks_list = tasks_list.filter(Task.assigned_by_user.has(first_name = value))
        elif key == "creation_date_start":
            tasks_list = tasks_list.filter(Task.creation_date >= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "creation_date_end":
            tasks_list = tasks_list.filter(Task.creation_date <= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "deadline_start":
            tasks_list = tasks_list.filter(Task.deadline >= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "deadline_end":
            tasks_list = tasks_list.filter(Task.deadline <= datetime.datetime.strptime(value, "%Y-%m-%d"))
        elif key == "are_assignees_or":
            if not collaborators_input_is_valid(value)[1]:
                continue
            value_list = collaborators_input_is_valid(value)[0]
            tasks_list = tasks_list.filter(
                or_(*[Task.current_assignees.any(User.id == user.id) for user in value_list])
            )
        elif key == "are_assignees_and":
            if not collaborators_input_is_valid(value)[1]:
                continue
            value_list = collaborators_input_is_valid(value)[0]
            for user in value_list:
                tasks_list = tasks_list.filter(Task.current_assignees.any(User.id == user.id))
        elif key == "status":
            if value not in STATUS_PERMITTED:
                continue
            boolean_status = (value == "OPEN")
            tasks_list = tasks_list.filter(Task.status == boolean_status)
        elif key == "priority_sort":
            if value not in SORT_PERMITTED:
                continue
            elif value == "ASC":
                tasks_list = tasks_list.order_by(Task.priority)
            elif value == "DESC":
                tasks_list = tasks_list.order_by(desc(Task.priority))
        elif key == "creation_date_sort":
            if value not in SORT_PERMITTED:
                continue
            elif value == "ASC":
                tasks_list = tasks_list.order_by(Task.creation_date)
            elif value == "DESC":
                tasks_list = tasks_list.order_by(desc(Task.creation_date))
        elif key == "deadline_sort":
            if value not in SORT_PERMITTED:
                continue
            elif value == "ASC":
                tasks_list = tasks_list.order_by(Task.deadline)
            elif value == "DESC":
                tasks_list = tasks_list.order_by(desc(Task.deadline))
        elif key == "status_sort":
            if value not in STATUS_SORT_PERMITTED:
                continue
            elif value == "OPEN_FIRST":
                tasks_list = tasks_list.order_by(desc(Task.status))
            elif value == "CLOSED_FIRST":
                tasks_list = tasks_list.order_by(Task.status)

    return tasks_list
