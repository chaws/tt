from enum import Enum
from minivenmo.exceptions import UsernameException, PaymentException
import re
import uuid


class Methods(Enum):
    BALANCE = 1
    CREDIT_CARD = 2


class Payment:

    def __init__(self, amount, actor, target, note, method):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note
        self.method = method
 

class User:

    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0
        self.friends = {}

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException('Username not valid')

    def retrieve_feed(self):
        # TODO: add code here
        return []

    def add_friend(self, friend):
        assert friend is not None

        if friend.username in self.friends:
            print(f"I: {friend} is already added to the list of {self.username}'s friends")
            return

        print(f"I: Adding {friend} to the list of {self.username}'s friends")
        self.friends[friend.username] = friend

    def add_to_balance(self, amount):
        print(f"I: Adding {amount:.2f} to {self} funds")
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        print(f"I: Adding credit card to {self}")
        if self.credit_card_number is not None:
            raise CreditCardException('Only one credit card per user!')

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException("Invalid credit card number.")

    def pay(self, target, amount, note):
        print(f"I: {self} is paying {target} the amount of {amount:.2f} regarding \"{note}\"")
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException("Users cannot pay themselves.")

        elif amount <= 0.0:
            raise PaymentException("Amount must be a non-negative number.")
        
        method = None
        if amount <= self.balance:
            self.pay_with_balance(amount)
            method = Methods.BALANCE
        else:
            self.pay_with_card(target, amount)
            method = Methods.CREDIT_CARD

        payment = Payment(amount, self, target, note, method)
        target.add_to_balance(amount)
        return payment

    def pay_with_card(self, target, amount):
        if self.credit_card_number is None:
            raise PaymentException("Must have a credit card to make a payment.")

        self._charge_credit_card(self.credit_card_number, target, amount)

    def pay_with_balance(self, amount):
        if self.balance < amount:
            raise PaymentException("Not enough funds to make payment!")

        self.balance -= amount

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match('^[A-Za-z0-9_\\-]{4,15}$', username)

    def _charge_credit_card(self, credit_card_number, target, amount):
        # magic method that charges a credit card thru the card processor
        pass

    def __str__(self):
        return self.username

