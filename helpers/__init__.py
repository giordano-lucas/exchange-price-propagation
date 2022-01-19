import yaml
import os


dirname = os.path.dirname(__file__)
config_file = os.path.join(dirname, 'config.yml')
with open(config_file, 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
