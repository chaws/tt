from minivenmo.models import User
from minivenmo.exceptions import UsernameException, PaymentException
from unittest.mock import patch
import unittest


VALID_CREDIT_CARD_NUMBER = "4242424242424242"


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

    @patch("minivenmo.models.User._charge_credit_card")
    def test_pay_with_card_no_credit_card(self, mock_charge_credit_card):
        """
        Ensure exception is raise when no credit card present
        """

        user = User("user")
        with self.assertRaises(PaymentException) as ctx:
            user.pay_with_card(None, None)

        self.assertEqual("Must have a credit card to make a payment.", str(ctx.exception))
        mock_charge_credit_card.assert_not_called()

    @patch("minivenmo.models.User._charge_credit_card")
    def test_pay_with_card(self, mock_charge_credit_card):
        """
        Ensure to charge credit card when available
        """

        user = User("user")
        user.add_credit_card(VALID_CREDIT_CARD_NUMBER)
        target = User("target")
        amount = 42.0
        user.pay_with_card(target, amount)
        mock_charge_credit_card.assert_called_with(user.credit_card_number, target, amount)

    def test_pay_with_balance_not_enough_funds(self):
        """
        Ensure enough funds to pay with balance 
        """

        user = User("user")
        with self.assertRaises(PaymentException) as ctx:
            user.pay_with_balance(42.0)

        self.assertEqual("Not enough funds to make payment!", str(ctx.exception))

    def test_pay_themself(self):
        """
        Ensure users can't pay themselves
        """

        user = User("user")
        with self.assertRaises(PaymentException) as ctx:
            user.pay(user, 42, None)

        self.assertEqual("Users cannot pay themselves.", str(ctx.exception))

    def test_pay_non_positive_amount(self):
        """
        Ensure no negative or zero payments
        """

        user = User("user")
        target = User("target")
        with self.assertRaises(PaymentException) as ctx:
            user.pay(target, -42, None)

        self.assertEqual("Amount must be a non-negative number.", str(ctx.exception))
        self.assertEqual(0.0, target.balance)

        with self.assertRaises(PaymentException) as ctx:
            user.pay(target, 0, None)

        self.assertEqual("Amount must be a non-negative number.", str(ctx.exception))
        self.assertEqual(0.0, target.balance)

    @patch("minivenmo.models.User._charge_credit_card")
    @patch("minivenmo.models.User.pay_with_balance")
    def test_pay_use_credit_card(self, mock_pay_with_balance, mock_charge_credit_card):
        """
        Ensure to use credit card when not enough funds
        """

        user = User("user")
        user.add_credit_card(VALID_CREDIT_CARD_NUMBER)
        target = User("target")
        amount = 42

        user.pay(target, amount, None)

        self.assertEqual(amount, target.balance)
        mock_pay_with_balance.assert_not_called()
        mock_charge_credit_card.assert_called_with(VALID_CREDIT_CARD_NUMBER, target, amount)

    @patch("minivenmo.models.User._charge_credit_card")
    def test_pay_use_balance(self, mock_charge_credit_card):
        """
        Ensure to use balance that covers amount
        """

        amount = 42
        user = User("user")
        user.add_to_balance(42)
        user.add_credit_card(VALID_CREDIT_CARD_NUMBER)
        target = User("target")

        user.pay(target, amount, None)

        self.assertEqual(amount, target.balance)
        self.assertEqual(0.0, user.balance)
        mock_charge_credit_card.assert_not_called()
