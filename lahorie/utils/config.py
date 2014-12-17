# -*- coding: utf8 -*-

"""
    The ``config`` module
    =====================

    Create a named logger and  return it so users can log in different log files : one for each module.
"""

import os
import os.path as path
import errno
import sys

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import lahorie.utils.log

logger = lahorie.utils.log.get_logger('config')


def get_config(config_file_path=None, config_prefix='bot') -> dict:
    """
    Return the config from a yaml file as a dictionary. Create one file if not existing, using example file as template.

    :rtype : dict
    :param config_file_path:
    :return:
    """
    if config_file_path is None:
        config_dir_path = os.path.abspath(os.path.join(os.sep, os.path.expanduser("~"), '.botIrc', 'config'))
    else:
        config_dir_path = os.path.abspath(os.path.dirname(config_file_path))
    config_file_path = path.join(config_dir_path, '{}.config.yaml'.format(config_prefix))
    config_example_path = path.abspath(path.join(os.sep, path.dirname(__file__), path.pardir,
                                                 path.pardir, 'logs', '{}.example.yaml'.format(config_prefix)))
    try:
        with open(config_file_path, 'rb') as config_stream:
            config_dict = yaml.load(config_stream, Loader=Loader)
    except IOError:
        logger.info('')
        try:
            os.makedirs(config_dir_path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and path.isdir(config_dir_path):
                pass
            else:
                raise
        with open(config_file_path, 'a'):
            os.utime(config_file_path, None)
        try:
            with open(config_example_path, 'rb') as config_example_stream:
                config_dict_example = yaml.load(config_example_stream, Loader=Loader)
            # TODO : console based example file modification
            with open(config_file_path, 'wb') as config_stream:
                yaml.dump(config_dict_example, config_stream, Dumper=Dumper, encoding='utf-8')
        except IOError:
            logger.critical("No example file. Exiting.")
            sys.exit(0)
        try:
            with open(config_file_path, 'rb') as config_stream:
                config_dict = yaml.load(config_stream, Loader=Loader)
        except IOError:
            sys.exit(0)
    return config_dict