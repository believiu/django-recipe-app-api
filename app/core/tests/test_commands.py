from unittest import TestCase
from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError


class CommandTest(TestCase):
    def test_wait_for_db_ready(self):
        """Test that we wait for db to be available"""
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            gi.return_value = True
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, 1)

    def test_wait_for_db(self):
        """Test waiting for DB """
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            with patch("time.sleep") as sleep:
                sleep.return_value = True
                gi.side_effect = [OperationalError] * 4 + [True]
                call_command("wait_for_db")
                self.assertEqual(gi.call_count, 5)
