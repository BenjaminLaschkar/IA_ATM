"""
------------------------------------------------------------------------------.

configProxy.py is a library to get all the changing parameter of the wall-e.

-------------------------------------------------------------------------------
"""
import yaml
path_to_file = "/home/pi/Desktop/Distributeur/setting/config.yml"
with open(path_to_file, 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)


def getIp():
    """Get the local IP adress of the wall-e."""
    return config["ip_adress"]


def getPort():
    """Get the local port adress for the behavior manager of the wall-e."""
    return config["port"]
