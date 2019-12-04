#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `trello_release_notes` package that don't use the network.
For testing when you're in the subway.
pytest fixtures are defined in conftest.py
"""

import pytest


expected_summary = """- card headline 0
- card headline 1
- card headline 2
- card headline 3"""

expected_members_summary = """- card headline 0 ['fo', 'ob', 'ar']
- card headline 1 
- card headline 2 ['fo', 'ob', 'ar']
- card headline 3 """



def test_summarize_these_cards_with_members(trellist, sample_member_cards):
    summary = trellist.summarize_these(
        sample_member_cards,
        template="- {card.name} {card.members_initials}",
        prep_function=lambda discard, x: x,
    )
    assert expected_members_summary == summary


def test_summarize_these_cards(trellist, sample_cards):
    summary = trellist.summarize_these(
        sample_cards, template="- {card.name}", prep_function=lambda discard, x: x
    )
    assert expected_summary == summary


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
