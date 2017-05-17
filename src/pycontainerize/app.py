import json
from json import JSONEncoder
import os
from constants import (
    APP_TEMPLATE_MAP,
    APP_CONFIG,
    APP_ATTRIB,
    CONTEXT_ATTRIB,
    PROJECT_ATTRIB,
    DOMAIN_ATTRIB,
    SERVICE_ATTRIB,
)
from errors import (
    UnableToLoadApp,
    UnableToRenderTemplate,
)


class AppEncoder(JSONEncoder):
    ''' Encode an App object into a dict for JSON serialization '''
    def default(self, obj):
        return obj.app


class App(object):
    ''' A python web app '''
    def __init__(self, app):
        self.app = app

    @staticmethod
    def load(app_dir):
        app_file = os.path.join(app_dir, APP_CONFIG)
        try:
            with open(app_file, "r") as appfp:
                app = json.load(appfp)
                return App(app)
        except Exception as err:
            raise UnableToLoadApp(app_file + ': ' + str(err))

    def __str__(self):
        return json.dumps(
            self,
            cls=AppEncoder,
            ensure_ascii=True,
            indent=4,
            separators=(': ', ','),
        )

    def render(self,
               project,
               domain,
               renderer,
               output_dir):
        context = {}
        context[CONTEXT_ATTRIB] = APP_ATTRIB
        context[APP_ATTRIB] = dict(self.app.items())
        context[SERVICE_ATTRIB] = context[APP_ATTRIB]
        context[PROJECT_ATTRIB] = project
        context[DOMAIN_ATTRIB] = domain
        for (src, dst) in APP_TEMPLATE_MAP.items():
            try:
                dst = renderer.render_template_from_string(
                    dst,
                    context
                )
                output_path = os.path.join(output_dir, dst)
                output_parent = os.path.dirname(output_path)
                if not os.path.exists(output_parent):
                    os.makedirs(output_parent)
                renderer.render_template(src,
                                         context,
                                         output_path)
            except Exception as err:
                raise UnableToRenderTemplate(src + ': ' + str(err))

    def to_dict(self):
        return AppEncoder().default(self)
