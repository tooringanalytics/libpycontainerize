from json import JSONEncoder
import json


class NetworkEncoder(JSONEncoder):
    ''' Encode a Network object into a dict for JSON serialization '''
    def default(self, obj):
        nw = {}
        network = obj.network
        for key in network.keys():
            nw[key] = network[key]
        return nw


class Network(object):
    ''' Networks Config '''
    def __init__(self, project_dir, network_def):
        self.network = network_def
        self.dir = project_dir


class Networks(object):

    ''' Networks Config '''
    def __init__(self, project_dir, networks_def):
        self.networks = networks_def
        self.dir = project_dir

    @staticmethod
    def load(project_dir, networks_def):
        return Networks(project_dir, networks_def)
        '''
        networks_file = os.path.join(project_dir, NETWORKS_CONFIG)
        try:
            with open(networks_file, "r") as nwfp:
                networks_def = json.load(nwfp)
                return Networks(project_dir, networks_def)
        except UnableToLoadApp:
            raise
        except IOError as err:
            return Networks(project_dir, [])
        except Exception as err:
            raise UnableToLoadNetworksConfig(networks_file + ': ' + str(err))
        '''

    def to_python(self):
        return self.to_dict()

    def to_dict(self):
        return self.networks

    def __str__(self):
        return json.dumps(
            self.networks,
            ensure_ascii=True,
            indent=4,
            sort_keys=True,
            separators=(',', ': '),
        )
