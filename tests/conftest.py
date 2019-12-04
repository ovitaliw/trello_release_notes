#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Fixtures for tests"""

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


# scope at module level to avoid extra get_board calls
@pytest.fixture(scope="module")
def trellist():
    trellist = Trellist(
        args.apikey, args.apisecret, args.boardname, args.done_list, args.releases
    )
    return trellist


@pytest.fixture
def sample_member_cards():
    Card = namedtuple(
        "Card",
        "name description url members_initials members_full_names members_usernames",
    )
    samples = []
    for num in range(0, 4):
        members_initials = ""
        if num % 2 == 0:
            members_initials = ["fo", "ob", "ar"]
        samples.append(
            Card(
                f"card headline {num}",
                f"card description {num}",
                f"http://example.com/{num}",
                members_initials,
                "",
                "",
            )
        )
    return samples


@pytest.fixture
def sample_cards():
    Card = namedtuple("Card", "name description url")
    samples = []
    for num in range(0, 4):
        samples.append(
            Card(
                f"card headline {num}",
                f"card description {num}",
                f"http://example.com/{num}",
            )
        )
    return samples

