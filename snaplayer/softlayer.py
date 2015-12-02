# -*- coding: utf-8 -*-

"""
snaplayer.softlayer
~~~~~~~~

softlayer dealer

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

import SoftLayer
from . import log
from .config import Config

def capture(config_file, *, dry_run=False):
    # read config file
    config = Config(config_file=config_file)

    # Connect to service using credentials
    log.msg("Connecting to SoftLayer service ...")
    if not dry_run:
        sl_client = SoftLayer.create_client_from_env()
    log.msg("Connection to SoftLayer succesful!")


    log.msg("Looking for instances with following properties:")
    for key, value in config.options.items():
        log.msg("* [{:10}] -> '{}'".format(key, value))

    # list instances
    if not dry_run:
        sl_vs_mgr = SoftLayer.VSManager(sl_client)
        instances = sl_vs_mgr.list_instances(**config.options)
        for vsi in instances:
            log.msg(vsi)

    # capture each instance
