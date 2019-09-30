# -*- coding: utf-8 -*-

"""Main module."""
from datetime import date
from trello import TrelloClient
from loguru import logger

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
    def __init__(
        self,
        apikey,
        apisecret,
        boardname,
        done_list_name="done",
        releases_list_name="releases",
        create_comments=True,
        create_release_if_zero_done=False,
    ):
        """Ah the init method.

        :param apikey:
        :param apisecret:
        :param boardname:
        :param done_list_name:
        :param releases_list_name:
        """
        self.client = TrelloClient(api_key=apikey, api_secret=apisecret)
        self.board = self.get_board(boardname)
        self.done = self.get_list_by_name(done_list_name)
        self.releases = self.get_list_by_name(releases_list_name)
        self.release_template = "{date} release: {count} done"
        self.create_comment_per_item = create_comments
        self.create_release_if_zero_done = create_release_if_zero_done

    def run(self):
        logger.info(f"get all cards in the done board: {self.done.name}")
        cards = self.get_done_cards()
        logger.info(f"got {len(cards)} cards")
        if cards or self.create_release_if_zero_done:
            release_card = self.create_release_card(self.release_template, cards)
            for card in cards:
                if self.create_comment_per_item:
                    self.add_comment_to_release(release_card, card)
                card.set_closed(True)
        logger.info("finished run")

    def get_board(self, board_name):
        """Gets the open board object by a name, otherwise returns None

        :param board_name:
        """
        return self.first(
            self.client.list_boards(), lambda b: b.name == board_name and not b.closed
        )

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
        release_card_name = template.format(
            date=date.today().isoformat(), count=len(cards)
        )
        # turn list of names of cards into a summary
        summary = self.summarize_these(cards)
        logger.info(f"{summary}")
        release_card = self.releases.add_card(release_card_name, summary)
        return release_card

    def add_comment_to_release(self, release_card, card, comment_format=None):
        if comment_format is None:
            comment_format = "{card.name}\n{card.url}\n{card.description}"
        comment_text = comment_format.format(card=card)
        release_card.comment(comment_text)
