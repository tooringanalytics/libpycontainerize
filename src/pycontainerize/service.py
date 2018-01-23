import json
import os
import sys
from json import JSONEncoder

import six
from pycontainerize.constants import SERVICE_ATTRIB
from pycontainerize.constants import SERVICE_CONFIG
from pycontainerize.constants import SERVICE_TEMPLATE_MAP
from pycontainerize.constants import THIS_ATTRIB
from pycontainerize.errors import UnableToLoadService


class ServiceEncoder(JSONEncoder):
    ''' Encode a Service object into a dict for JSON serialization '''

    def default(self, obj):
        return obj.service


class Service(object):
    ''' A service for a given domain '''

    def __init__(self, service):
        self.service = service

    @staticmethod
    def load(service_dir):
        service_file = os.path.join(service_dir, SERVICE_CONFIG)
        try:
            with open(service_file, "r") as svcfp:
                service = json.load(svcfp)
                return Service(service)
        except Exception as err:
            raise UnableToLoadService(service_file + ': ' + str(err))

    def __str__(self):
        return json.dumps(
            self,
            cls=ServiceEncoder,
            ensure_ascii=True,
            indent=4,
            separators=(': ', ','),
        )

    def render(self,
               context,
               renderer,
               output_dir):
        context_copy = dict(context.items())
        context = context_copy
        # Save a copy of this object's attribs in the context
        context[SERVICE_ATTRIB] = dict(self.service.items())
        context[THIS_ATTRIB] = context[SERVICE_ATTRIB]
        for (src, dst) in SERVICE_TEMPLATE_MAP.items():
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
                six.reraise(type(err), err, sys.exc_info()[2])
                # raise UnableToRenderTemplate(src + ': ' + str(err))

    def to_dict(self):
        return ServiceEncoder().default(self)
