from minivenmo import MiniVenmo
from minivenmo.exceptions import UsernameException
import unittest


INVALID_CREDIT_CARD_NUMBER = "123"
VALID_CREDIT_CARD_NUMBER = "4242424242424242"


class TestMiniVenmo(unittest.TestCase):

    def setUp(self):
        self.venmo = MiniVenmo()

    def test_create_user_username_already_exists(self):
        username = "username1"
        self.venmo.create_user(username, 1, VALID_CREDIT_CARD_NUMBER)

        with self.assertRaises(UsernameException) as ctx:
            self.venmo.create_user(username, 1, VALID_CREDIT_CARD_NUMBER)

        self.assertEqual(f"Username `{username}` already exists", str(ctx.exception))
