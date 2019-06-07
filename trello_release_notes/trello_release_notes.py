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
