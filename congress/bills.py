"""Module to manage congressional bill data."""

class Bill(object):
    """An instance of a congressional bill."""

    def __init__(self, congress, latest_action):
        self.congress = congress
        self.latest_action = latest_action
