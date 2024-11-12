"""Module to manage congressional bill data."""

class Bill(object):
    """An instance of a congressional bill."""

    def __init__(self, congress, latest_action, number, origin_chamber, title,
                 bill_type, update_date, update_including_text, url):
        self.congress = congress
        self.latest_action = latest_action
        self.number = number
        self.origin_chamber = origin_chamber
        self.title = title
        self.bill_type = bill_type
        self.update_date = update_date
        self.update_including_text = update_including_text
        self.url = url
