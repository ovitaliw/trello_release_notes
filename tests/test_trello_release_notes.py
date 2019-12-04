#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `trello_release_notes` package."""

import pytest


from trello_release_notes.trello_release_notes import Trellist
from trello_release_notes.__main__ import get_arg_parser
from collections import namedtuple
from pathlib import Path

test_ini = Path("tests/trello_test_settings.ini")
args = None
if test_ini.exists():
    args = get_arg_parser().parse_args(["--config", str(test_ini)])
else:
    Args = namedtuple("Args", "apikey apisecret boardname done_list releases")
    from os import environ

    args = Args(
        environ["apikey"],
        environ["apisecret"],
        environ["boardname"],
        environ["done_list"],
        environ["releases"],
    )

boardname = args.boardname
done_name = args.done_list
expected_summary = """- card headline 0
- card headline 1
- card headline 2
- card headline 3"""

expected_members_summary = """- card headline 0 ['fo', 'ob', 'ar']
- card headline 1 
- card headline 2 ['fo', 'ob', 'ar']
- card headline 3 """



def test_get_board(trellist):
    # let's connect and get a board
    board = trellist.get_board(boardname)
    assert board is not None
    assert board.name == boardname


def test_get_list_by_name(trellist):
    trello_list = trellist.get_list_by_name(done_name)
    assert trello_list.name == done_name


def test_get_done_cards(trellist):
    # need to set up and insert done cards for the test
    for num in range(0, 4):
        trellist.done.add_card(f"card {num}", f"description {num}")
    done_cards = trellist.get_done_cards()
    # tear down - remove every card on the list
    trellist.done.archive_all_cards()
    assert len(done_cards) == 4


def test_create_release_card(trellist, sample_member_cards):
    trellist.prep_card = lambda discard, x: x
    card = trellist.create_release_card(
        sample_member_cards, trellist.release_template, trellist.card_summary_template
    )
    assert card.description == expected_members_summary
    expected_card_sample_count = "{}".format(len(sample_member_cards))
    count_from_name = card.name.split(" ")[2]
    card.delete()
    assert count_from_name == expected_card_sample_count


def test_add_comment_to_release(trellist, sample_cards):
    card = sample_cards[0]

    class ReleaseCard:
        def comment(self, text):
            self.comment_text = text

    rc = ReleaseCard()
    trellist.add_comment_to_release(rc, card)
    assert (
        rc.comment_text == "card headline 0\nhttp://example.com/0\ncard description 0"
    )
