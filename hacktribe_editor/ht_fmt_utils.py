from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
import json
import yaml
import construct


@log_debug
def build_dict(fmt, dic):
    return fmt.build(dic)


@log_debug
def parse_bytes(fmt, byts):
    return fmt.parse(byts)


@log_debug
def refresh_struct(fmt, dic):
    return fmt.parse(fmt.build(dic))


@log_debug
def init_struct(fmt):
    return fmt.parse(fmt.build({}))


@log_debug
def remove_hidden_keys(dic):
    return {k: v for k, v in dic.items() if not k.startswith('_')}


@log_debug
def filter_dict(fmt, dic, remove=False):
    if remove:
        if isinstance(remove, str):
            remove = [remove]
        dic = recursive_filter(dic, remove)
    return container_to_dict(remove_hidden_keys(refresh_struct(fmt, dic)))


@log_debug
def get_key_index(dic, key):
    dic = remove_hidden_keys(dic)
    return list(dic.keys()).index(key)


@log_debug
def swap_key_value(dic):
    return dict((v, k) for k, v in dic.items())


@log_debug
def dict_to_yaml(dic, filepath):
    '''Write dict to filepath as yaml.'''
    Path(filepath).write_text(yaml.dump(dic))


@log_debug
def yaml_to_dict(filepath):
    '''Return dict forom yaml at filepath.'''
    return yaml.safe_load(Path(filepath).read_text())


@log_debug
def container_to_yaml(container, filepath):
    '''Write container filepath as yaml'''
    dict_to_yaml(container_to_dict(container), filepath)


@log_debug
def yaml_to_container(yml, fmt):
    return dict_to_container(yaml_to_dict(yml), fmt)


@log_debug
def json_to_container(jsn, fmt):
    return dict_to_container(json_to_dict(jsn), fmt)


@log_debug
def json_to_dict(jsn):
    return json.load(jsn)


@log_debug
def container_to_namespace(container):
    return SimpleNamespace(**container_to_dict(container))


@log_debug
def dict_to_container(fmt, dic):
    return fmt.parse(fmt.build(dic))


@log_debug
def container_to_dict(cont):

    dic = {}
    for e in cont:
        if isinstance(cont[e], construct.core.EnumIntegerString):
            dic[e] = str(cont[e])

        elif isinstance(cont[e], construct.core.EnumInteger):
            dic[e] = int(cont[e])

        elif isinstance(cont[e], construct.core.Container):
            dic[e] = container_to_dict(cont[e])

        elif isinstance(cont[e], construct.core.ListContainer):
            dic[e] = [container_to_dict(i) for i in cont[e]]

        elif isinstance(cont[e], construct.lib.containers.ListContainer):
            dic[e] = [container_to_dict(i) for i in cont[e]]

        elif isinstance(cont[e], str):
            dic[e] = cont[e]

        elif isinstance(cont[e], int):
            dic[e] = cont[e]

        elif isinstance(cont[e], bytes):
            dic[e] = cont[e]

    return dic


@log_debug
def open_bin(path):
    with open(path, 'rb') as file:
        return file.read()


@log_debug
def open_file(path):
    with open(path, 'r') as file:
        return file.read()


@log_debug
def yaml_to_bin(path, fmt):
    '''Return bytes from yaml at path in format fmt'''

    yml = open_file(path)
    cont = yaml_to_container(yml, fmt)
    return fmt.build(cont)


@log_debug
def json_to_bin(path, fmt):
    '''Return bytes from json at path in format fmt'''

    jsn = open_file(path)
    cont = json_to_container(jsn, fmt)
    return fmt.build(cont)


@log_debug
def recursive_filter(dic, remove):
    return dic
