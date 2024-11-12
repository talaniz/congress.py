"""Module to manage congressional bill data."""

from collections import namedtuple

Bill = namedtuple('Bill', ['congress', 'latest_action', 'number', 'origin_chamber',
                           'title', 'bill_type', 'update_date', 'update_including_text', 'url'])
