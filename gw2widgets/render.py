# render pages

from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

class Render:
    __borg_state = {}

    def __init__(self, config):
        self.__dict__ = self.__borg_state
        self.config = config

    def render(self, page_id, filename, data):
        """Render a page

        Params:
            page_id  = The page ID for the page to generate
            filename = The output filename (sans path)
            data     = The data for the page
        """
