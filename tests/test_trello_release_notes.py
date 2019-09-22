#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `trello_release_notes` package."""

import pytest


from trello_release_notes.trello_release_notes import Trellist
from trello_release_notes.__main__ import get_args
from collections import namedtuple

args = get_args(["--config", "tests/trello_test_settings.ini"])
boardname = args.boardname
done_name = args.done_list
releases_name = args.releases
expected_summary = \
"""- card headline 0
- card headline 1
- card headline 2
- card headline 3"""


@pytest.fixture
def sample_cards():
    Card = namedtuple("Card", "name description")
    samples = []
    for num in range(0,4):
        samples.append(Card(f"card headline {num}", f"card description {num}"))
    return samples

# scope at module level to avoid extra get_board calls
@pytest.fixture(scope="module")
def trellist():
    return Trellist(args.apikey, args.apisecret, args.boardname, args.done_list, args.releases)


def test_summarize_these_cards(sample_cards):
    summary = Trellist.summarize_these(sample_cards)
    assert expected_summary == summary

def test_get_board(trellist):
    #let's connect and get a board
    board = trellist.get_board(boardname)
    assert board is not None
    assert board.name == boardname

def test_get_list_by_name(trellist):
    l = trellist.get_list_by_name(done_name)
    assert l.name == done_name

def test_get_done_cards(trellist):
    # need to set up and insert done cards for the test
    for num in range(0,4):
        trellist.done.add_card(f"card {num}", f"description {num}")
    done_cards = trellist.get_done_cards()
    # tear down - remove every card on the list
    trellist.done.archive_all_cards()
    assert len(done_cards) == 4

def test_create_release_card(trellist, sample_cards):
    card = trellist.create_release_card(trellist.release_template, sample_cards)
    assert card.description == expected_summary
    expected_card_sample_count = "{}".format(len(sample_cards))
    count_from_name = card.name.split( " ")[2]
    card.delete()
    assert count_from_name == expected_card_sample_count
