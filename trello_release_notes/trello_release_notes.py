# -*- coding: utf-8 -*-

"""Main module."""
from trello import TrelloClient

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
        self.done = done_list_name
        self.releases = releases_list_name
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
        summary = self.summarize_these(cards)
        release_card = self.create_release_card(self.release_template, summary)
        for card in cards:
            if self.create_comment_per_item:
                self.add_comment_to_release(release_card, card)
            self.archive_card(card)

    def get_board(self, board_name):
        remote_boards = self.client.list_boards()
        for board in remote_boards:
            if board.closed:
                continue
            if board.name == board_name:
                return board
        return None

    def get_done_cards(self):
        raise NotImplementedError

    @classmethod
    def summarize_these(self, cards):
        raise NotImplementedError
