#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `trello_release_notes` package."""

import pytest


from trello_release_notes import trello_release_notes


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


def test_summarize_these_cards(sample_cards):
    summary = trello_release_notes.Trellist.summarize_these(sample_cards)
    assert sample_cards == summary



