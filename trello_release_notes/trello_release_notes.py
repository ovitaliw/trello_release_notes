# -*- coding: utf-8 -*-

"""Main module."""
from trello import TrelloClient
from datetime import date

"""
# given a list of boards
# for each board
# given a "done" list
# given a "released" list
# if there are items in the done list,
    create a release card for this date in the releases list
# for each item in the done list
# get the release card for this date
# append the title as list item to the description of the release card
# add the title and details as a comment on the release card
# archive the done item
# post process - send an email or do something with the release detail
"""


class Trellist(object):
    def __init__(self, apikey, apisecret, boardname, done_list_name="done", releases_list_name="releases"):
        self.client = TrelloClient(api_key=apikey, api_secret=apisecret)
        self.board = self.get_board(boardname)
        self.done = self.get_list_by_name(done_list_name)
        self.releases = self.get_list_by_name(releases_list_name)
        self.release_template = "{date} release: {count} done"
        self.create_comment_per_item = True

    def cards_to_data(self, cards):
        """returns a dict of card data

        :param cards: list of card objects
        """
        raise NotImplementedError

    def run(self):
        # get all cards in the done board
        cards = self.get_done_cards()
        release_card = self.create_release_card(self.release_template, cards)
        for card in cards:
            if self.create_comment_per_item:
                self.add_comment_to_release(release_card, card)
            self.archive_card(card)

    def get_board(self, board_name):
        """Gets the open board object by a name, otherwise returns None

        :param board_name:
        """
        return self.first(self.client.list_boards(), lambda b: b.name == board_name and not b.closed)

    def get_list_by_name(self, name):
        """iterate lists and get the first one matching the name passed in

        :param name:
        """
        return self.first(self.board.list_lists(), lambda l: l.name == name)

    def first(self, iterable, condition):
        """iterates an iterable and returns the first item that meets a condition or None

        :param iterable:
        :param condition:
        """
        return next((i for i in iterable if condition(i)), None)

    def get_done_cards(self):
        return self.done.list_cards()

    @classmethod
    def summarize_these(self, cards):
        summary = "\n".join([f"- {card.name}" for card in cards])
        return summary

    def create_release_card(self, template, cards):
        release_card_name = template.format(date=date.today().isoformat(), count=len(cards))
        # turn list of names of cards into a summary
        summary = self.summarize_these(cards)
        release_card = self.releases.add_card(release_card_name, summary)
        return release_card
