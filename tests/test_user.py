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

    def test_add_null_friend(self):
        """
        Ensure friend is not None
        """

        user = User("user")
        with self.assertRaises(AssertionError):
            user.add_friend(None)

    def test_add_friend(self):
        """
        Ensure friend is added to user's friends list
        """

        user = User("user")
        friend = User("friend")
        user.add_friend(friend)
        self.assertEqual(1, len(user.friends))
        self.assertTrue(friend, user.friends)

    def test_add_friend_already_added(self):
        """
        Ensure to avoid adding same friend twice to user's friends list
        """

        user = User("user")
        friend = User("friend")

        # Add first time
        user.add_friend(friend)
        self.assertEqual(1, len(user.friends))
        self.assertTrue(friend, user.friends)

        # Add again, noop
        user.add_friend(friend)
        self.assertEqual(1, len(user.friends))
        self.assertTrue(friend, user.friends)
