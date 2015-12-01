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
        with open(config_file, "r") as file:
            data = yaml.load(file)
            for key, value in data.items():
                if key in self._options:
                    self._options[key] = value

    @property
    def options(self):
        return self._options
