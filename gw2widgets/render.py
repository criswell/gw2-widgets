# render pages

from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from jinja2.ext import Extension
from jinja2 import nodes
from gw2api import GW2_API

class PrintCoin(Extension):
    tags = set(['coins'])

    def __init__(self, environment):
        super(PrintCoin, self).__init__(environment)

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = [parser.parse_expression()]

        return nodes.CallBlock(self.call_method('_print_coins', args),
                               [], [], []).set_lineno(lineno)

    def _print_coins(self, value, caller):
        print caller
        print value
        return "<!--{0}-->".format(value)

class Render:
    __borg_state = {}

    def __init__(self, config):
        self.__dict__ = self.__borg_state
        self.config = config
        self.output = self.config['output-dir']
        self.source = self.config['source-dir']
        self.env = Environment(extensions=[PrintCoin])
        self.env.loader = FileSystemLoader(self.config['template-dirs'])
        self.api = GW2_API(config)
        self.coins = {
            'gold' : self.api.get("files", { 'ids' : 'ui_coin_gold' }),
            'silver' : self.api.get("files", { 'ids' : 'ui_coin_silver' }),
            'copper' : self.api.get("files", { 'ids' : 'ui_coin_copper' })
            }

    def render(self, page_id, filename, data):
        """Render a page

        Params:
            page_id  = The page ID for the page to generate
            filename = The output filename (sans path)
            data     = The data for the page
        """
        with open("{0}/{1}.html".format(self.source, page_id),
                "r") as tf:
            raw_template = ''.join(tf.readlines())
            template = self.env.from_string(raw_template)
            rendered = template.render(data=data)
            with open("{0}/{1}".format(self.output, filename), 'w') as of:
                of.write(rendered)
