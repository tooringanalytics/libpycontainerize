from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2.ext import with_


class Renderer(object):
    ''' Template renderer, uses Jinja2 '''

    def __init__(self, templates_dir):
        self.templates_dir = templates_dir
        self.jinja = self.init_template_engine(templates_dir)

    def init_template_engine(self, templates_dir):
        jinja_env = Environment(
            loader=FileSystemLoader(templates_dir),
            extensions=[with_],
            lstrip_blocks=True,
            trim_blocks=True,
        )
        return jinja_env

    def render_template_from_string(self,
                                    source,
                                    context):
        template = self.jinja.from_string(source)
        return template.render(**context)

    def render_template(self,
                        template_file,
                        context,
                        output_path,
                        print_file=True):
        template = self.jinja.get_template(template_file)
        # First Pass
        output_text = template.render(**context)
        # Second Pass (resolves parameterized values)
        output_text = self.render_template_from_string(output_text,
                                                       context)
        with open(output_path, "w") as ofp:
            ofp.write(output_text)
        if print_file:
            print(output_path)
