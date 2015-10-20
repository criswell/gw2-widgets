# render pages

from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

class Render:
    __borg_state = {}

    def __init__(self, config):
        self.__dict__ = self.__borg_state
        self.config = config
        self.output = self.config['output-dir']
        self.env = Environment()
        self.env.loader = FileSystemLoader(self.config['template_dirs'])

    def render(self, page_id, filename, data):
        """Render a page

        Params:
            page_id  = The page ID for the page to generate
            filename = The output filename (sans path)
            data     = The data for the page
        """
        with open("{0}/{1}.html".format(self.template_dir, page_id),
                "r") as tf:
            raw_template = tf.readlines()
            template = self.env.from_string(raw_template)
            rendered = template.render(data=data)
            with open("{0}/{1}".format(self.output, filename), 'w') as of:
                of.write(rendered)
