import yaml

class Config():

    """Docstring for . """

    def __init__(self, *, config_file):
        self._options = {
            'hourly': True,
            'monthly': True,
            'tags': None,
            'cpus': None,
            'memory': None,
            'hostname': None,
            'domain': None,
            'local_disk': None,
            'datacenter': None,
            'nic_speed': None,
            'public_ip': None,
            'private_ip': None
            }
        #
        self._schema = Schema({
            Optional('hourly'): bool,
            Optional('monthly'): bool,
            Optional('tags'): lambda tags: type(tags) is list and all([type(t) is str for t in tags]),
            Optional('cpus'): int,
            Optional('memory'): int,
            Optional('hostname'): str,
            Optional('domain'): str,
            Optional('local_disk'): str,
            Optional('datacenter'): str,
            Optional('nic_speed'): int,
            Optional('public_ip'): str,
            Optional('private_ip'): str
            })
        #
        with open(config_file, "r") as file:
            data = self._schema.validate(yaml.load(file))
            for key, value in data.items():
                if key in self._options:
                    self._options[key] = value

    @property
    def options(self):
        return self._options
