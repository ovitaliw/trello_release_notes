#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `trello_release_notes` package.
pytest fixtures are defined in conftest.py
"""

import pytest



expected_members_summary = """- card headline 0 ['fo', 'ob', 'ar']
- card headline 1 
- card headline 2 ['fo', 'ob', 'ar']
- card headline 3 """



def test_get_board(trellist, conf):
    # let's connect and get a board
    board = trellist.get_board(conf.boardname)
    assert board is not None
    assert board.name == conf.boardname


def test_get_list_by_name(trellist, conf):
    trello_list = trellist.get_list_by_name(conf.done_list)
    assert trello_list.name == conf.done_list


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


