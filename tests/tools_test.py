import unittest
from unittest.mock import MagicMock, patch
import datetime

# Import your functions
from Gouvernement.aux.tools import collaborators_input_is_valid, project_search, task_search
from main import app
from Gouvernement.models import *

class TestAuxiliaryTools(unittest.TestCase):

    @patch('Gouvernement.models.User')
    def test_collaborators_input_is_valid_empty(self, mock_user):
        collaborators, valid = collaborators_input_is_valid("")
        self.assertTrue(valid)
        self.assertEqual(collaborators, [])

    @patch('Gouvernement.models.User')
    def test_collaborators_input_is_valid_valid_email(self, mock_user):
        # Setup mock return for a valid user
        with app.app_context():
            mock_query = MagicMock()
            mock_user.query.filter_by.return_value = mock_query
            mock_query.first.return_value = "UserObject"

            collaborators, valid = collaborators_input_is_valid("valid@example.com")
            self.assertTrue(valid)
            self.assertEqual(collaborators, ["UserObject"])

    @patch('Gouvernement.models.User')
    def test_collaborators_input_is_valid_invalid_email(self, mock_user):
        # Setup mock to return None for an invalid user
        with app.app_context():
            mock_query = MagicMock()
            mock_user.query.filter_by.return_value = mock_query
            mock_query.first.return_value = None

            collaborators, valid = collaborators_input_is_valid("invalid@example.com")
            self.assertFalse(valid)
            self.assertEqual(collaborators, [])

    def test_project_search_no_filters(self):
        # projects_list mock: filter returns self for chaining
        projects_list = MagicMock()
        projects_list.filter.return_value = projects_list

        result = project_search("", projects_list)
        self.assertEqual(result, projects_list)
        projects_list.filter.assert_not_called()

    def test_project_search_title_contains(self):
        projects_list = MagicMock()
        projects_list.filter.return_value = projects_list

        search_str = "title_contains=<Test Project>"
        result = project_search(search_str, projects_list)

        projects_list.filter.assert_called()
        self.assertEqual(result, projects_list)

    def test_task_search_priority_and_status(self):
        tasks_list = MagicMock()
        tasks_list.filter.return_value = tasks_list

        search_str = "priority=<3> status=<OPEN>"
        result = task_search(search_str, tasks_list)

        self.assertEqual(result, tasks_list)
        self.assertTrue(tasks_list.filter.call_count >= 2)

    # Additional tests would mock collaborators_input_is_valid within project_search and task_search
    @patch('Gouvernement.aux.tools.collaborators_input_is_valid')
    def test_project_search_are_collaborators(self, mock_collab_valid):
        projects_list = MagicMock()
        projects_list.filter.return_value = projects_list

        # Mock collaborators_input_is_valid to return dummy list
        mock_collab_valid.return_value = (["email@example.com"], True)

        search_str = "are_collaborators=<email@example.com>"
        result = project_search(search_str, projects_list)

        self.assertEqual(result, projects_list)
        self.assertTrue(projects_list.filter.called)

    # Test invalid attributes are ignored
    def test_task_search_unknown_attribute(self):
        tasks_list = MagicMock()
        tasks_list.filter.return_value = tasks_list

        search_str = "unknown_attr=<value> title_contains=<Hello>"
        result = task_search(search_str, tasks_list)

        self.assertEqual(result, tasks_list)
        tasks_list.filter.assert_called_once()  # Only one valid filter call

if __name__ == '__main__':
    unittest.main()
