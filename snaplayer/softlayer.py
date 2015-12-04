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
from datetime import datetime
from . import log
from .config import Config


def _connect(dry_run=False):
    """Connect to SoftLayer service

    :param dry_run: don't do anything
    """
    log.msg("Connecting to SoftLayer service ...")
    _sl_client = None
    if not dry_run:
        _sl_client = SoftLayer.create_client_from_env()
    log.msg("Connection to SoftLayer succesful!", bold=True)
    return _sl_client


def _generate_image_name():
    # Time in ISO8601 format
    now = datetime.now().isoformat()

    # Image UUID
    image_uuid = uuid.uuid4().hex

    # give the thing
    return "snaplayer-{}-{}".format(now, image_uuid)


def _capture_instance(vsi, *, sl_client, dry_run=False):
    """Capture all instances and create images from each one of them

    :param vsi: list of instances and their information
    """
    instance_id = vsi['id']
    log.msg_warn("Capturing instance #{}".format(instance_id))
    for k, v in vsi.items():
        log.msg_debug("    {:32} => {}".format(k, v))

    # generate image name for this instance
    image_name = _generate_image_name()

    log.msg("image name => '{}'".format(image_name), bold=True)
    if not dry_run:
        sl_vs_mgr = SoftLayer.VSManager(sl_client)
        capture_info = sl_vs_mgr.capture(instance_id, image_name)
        log.msg_debug('capture info: {}'.format(image_name))
        log.msg_debug(capture_info)

    # based on the averageTimeToComplete value,
    time_wait = math.floor(float(capture_info['transactionGroup']['averageTimeToComplete'])) * 60
    log.msg('Waiting for the transaction to finish ...')
    log.msg_warn('Maximum amount of time to wait: {} second(s)'.format(time_wait))
    if not dry_run:
        sl_vs_mgr.wait_for_transaction(instance_id, time_wait)


def _list_instances(config_file, *, sl_client, dry_run=False):
    # read config file
    config = _read_config_file(config_file)

    log.msg("Looking for instances with following properties:")
    for key, value in config.options.items():
        if value is not None:
            log.msg("* [{:10}] -> '{}'".format(key, value))

    # list instances
    if not dry_run:
        sl_vs_mgr = SoftLayer.VSManager(sl_client)
        instances = sl_vs_mgr.list_instances(**config.options)

        # check for number of instances
        if not len(instances):
            raise RuntimeError("No instance(s) matched with criteria " \
                    "specified on configuration file")
        else:
            log.msg("{} matching instance(s) found!".format(len(instances)), bold=True)

    return instances


def _read_config_file(config_file):
    log.msg("Reading configuration file: {}".format(config_file))
    return Config(config_file=config_file)


def _print_vsi_info(vsi):
    """List specified instances and their information on output"""
    instance_id = vsi['id']
    log.msg_warn("Instances will be listed only ...")
    log.msg("Instance: {}".format(instance_id), bold=True)
    for k, v in vsi.items():
        log.msg("    {:10} => {}".format(k, v))


def capture_instances(config_file, *, dry_run=False):
    """Generate images from instances"""

    # connect to softlayer, first of all
    sl_client = _connect(dry_run=dry_run)

    # Proceed with instance capture
    for vsi in _list_instances(config_file, sl_client=sl_client, dry_run=dry_run):
        # capture each instance
        _capture_instance(vsi, sl_client=sl_client, dry_run=dry_run)
    log.msg("Done!")


def list_instances(config_file, *, dry_run=False):
    """Generate images from instances"""

    # connect to softlayer, first of all
    sl_client = _connect(dry_run=dry_run)

    # print info about each instance
    for vsi in _list_instances(config_file, sl_client=sl_client, dry_run=dry_run):
        _print_vsi_info(vsi)
    log.msg("Done!")
