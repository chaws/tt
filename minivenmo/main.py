from minivenmo.models import User, Payment
from minivenmo.exceptions import PaymentException, UsernameException


class MiniVenmo:
    def __init__(self):
        self.__users = {}

    def create_user(self, username, balance, credit_card_number):
        if username in self.__users:
            raise UsernameException(f"Username `{username}` already exists")

        user = User(username)
        user.add_to_balance(balance)
        user.add_credit_card(credit_card_number)
        self.__users[username] = user
        return user

    def render_feed(self, feed):
        # Bobby paid Carol $5.00 for Coffee
        # Carol paid Bobby $15.00 for Lunch
        # TODO: add code here
        pass

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")
 
            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        venmo.render_feed(feed)

        bobby.add_friend(carol)
