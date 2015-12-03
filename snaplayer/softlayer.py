# -*- coding: utf-8 -*-

"""
snaplayer.softlayer
~~~~~~~~

softlayer dealer

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

import SoftLayer
import math
import uuid
from . import log
from .config import Config

# softlayer client
_sl_client = None


def connect(dry_run=False):
    """Connect to SoftLayer service

    :param dry_run: don't do anything
    """
    global _sl_client
    log.msg("Connecting to SoftLayer service ...")
    if not dry_run:
        _sl_client = SoftLayer.create_client_from_env()
    log.msg("Connection to SoftLayer succesful!", bold=True)


def _capture_instance(vsi, sl_vs_mgr):
    """Capture all instances and create images from each one of them

    :param vsi: list of instances and their information
    """
    instance_id = vsi['id']
    log.msg_warn("Capturing instance #{}".format(instance_id))
    image_name = "snaplayer-{}".format(uuid.uuid4().hex)

    log.msg("image name = {}".format(image_name))
    capture_info = sl_vs_mgr.capture(instance_id, image_name)
    log.msg(capture_info, bold=True)

    time_wait = math.floor(float(capture_info['transactionGroup']['averageTimeToComplete'])) * 60
    log.msg('Wait for the thing to be ready ...')
    log.msg('I will take no longer than {} seconds'.format(time_wait))
    sl_vs_mgr.wait_for_transaction(instance_id, time_wait)


def _list_instances(vsi):
    """List specified instances and their information on output"""
    instance_id = vsi['id']
    log.msg_warn("Instances will be listed only ...")
    log.msg("Instance: {}".format(instance_id), bold=True)
    for k, v in vsi.items():
        log.msg("    {:10} => {}".format(k, v))


def create_images(config_file, *, list_instances=True, dry_run=False):
    """Generate images from instances"""

    # read config file
    config = Config(config_file=config_file)

    log.msg("Looking for instances with following properties:")
    for key, value in config.options.items():
        if value is not None:
            log.msg("* [{:10}] -> '{}'".format(key, value))

    # list instances
    if not dry_run:
        sl_vs_mgr = SoftLayer.VSManager(_sl_client)
        instances = sl_vs_mgr.list_instances(**config.options)
        if not len(instances):
            raise RuntimeError("No instance found.")
        for vsi in instances:
            if not list_instances:
                # capture each instance
                _capture_instance(vsi, sl_vs_mgr)
            else:
                # list instances
                _list_instances(vsi)

            log.msg("Done!")
