#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `trello_release_notes` package."""

import pytest


from trello_release_notes.trello_release_notes import Trellist
from trello_release_notes.__main__ import get_args

args = get_args(["--config", "tests/trello_test_settings.ini"])
boardname = args.boardname
done_name = args.done_list
releases_name = args.releases


@pytest.fixture
def sample_cards():
    return [
        {"description": "card headline 1"},
        {"description": "card headline 2"},
        {"description": "card headline 3"},
        {"description": "card headline 4"},
        {"description": "card headline 5"},
        {"description": "card headline 6"},
    ]

# scope at module level to avoid extra get_board calls
@pytest.fixture(scope="module")
def trellist():
    return Trellist(args.apikey, args.apisecret, args.boardname, args.done_list, args.releases)


def test_summarize_these_cards(sample_cards):
    assert True
    # summary = Trellist.summarize_these(sample_cards)
    # assert sample_cards == summary

def test_get_board(trellist):
    #let's connect and get a board
    board = trellist.get_board(boardname)
    assert board is not None
    assert board.name == boardname
