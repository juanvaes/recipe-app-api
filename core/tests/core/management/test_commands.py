from unittest import mock

# psycopg2.OperationalError might be one of the errors that could be raised
# when we try to connect with the DB before the DB is ready
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


class TestCommands(SimpleTestCase):
    """Test commands"""

    @mock.patch("core.management.commands.wait_for_db.Command.check")
    def test_wait_for_is_ready(self, mocked_check):
        """Test waiting for database if database is ready"""
        mocked_check.return_value = True

        call_command("wait_for_db")

        mocked_check.assert_called_once_with(databases=['default'])

    @mock.patch("core.management.commands.wait_for_db.Command.check")
    @mock.patch("time.sleep")
    def test_wait_for_db_delay(self, mocked_sleep, mocked_check):
        """Test waiting for database when getting OperationalError"""
        mocked_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(mocked_check.call_count, 6)
        mocked_check.assert_called_with(databases=['default'])
