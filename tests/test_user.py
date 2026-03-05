from minivenmo.models import User
from minivenmo.exceptions import UsernameException
import unittest


class TestUser(unittest.TestCase):

    def test_create_user_invalid_username(self):
        """
        Ensure username validation happens
        """

        with self.assertRaises(UsernameException) as ctx:
            User("In valid")

        self.assertEqual("Username not valid", str(ctx.exception))
