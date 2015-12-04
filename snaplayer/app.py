# -*- coding: utf-8 -*-

"""
snaplayer.app
~~~~~~~~

Main module

:copyright: (c) 2015 by Alejandro Ricoveri
:license: MIT, see LICENSE for more details.

"""

import os
import sys
import traceback
import signal

from docopt import docopt
from docopt import DocoptExit

from snaplayer import __version__ as version
from snaplayer import PKG_URL as pkg_url
from snaplayer import __name__ as pkg_name
from snaplayer import log
from snaplayer import softlayer


def __parse_args(argv):
    """snaplayer

        Usage: snaplayer [options] (--list | --capture) <config>

        --ll=LVL, --log-level=LVL  Verbosity level on output [default: 1]
        -l=FILE, --log-file=FILE  Log file [default: snaplayer.log]
        -d, --dry-run  Dry run mode (don't do anything)
        -q, --quiet  Quiet output
        -h, --help  Print this message and exit
        -v, --version  Print version and exit
        --list  List instances only
        --capture  Capture instances and create images
    """
    return docopt(__parse_args.__doc__, argv=argv, version=version)


def init_parsecmdline(argv):
    """
    Parse arguments from the command line

    :param argv: list of arguments
    """
    return __parse_args(argv)


def _splash():
    """Print the splash"""
    splash_title = "{pkg} [{version}] - {url}".format(
        pkg=pkg_name, version=version, url=pkg_url)
    log.to_stdout(splash_title, colorf=log.yellow, bold=True)
    log.to_stdout('-' * len(splash_title), colorf=log.yellow, bold=True)


def init(argv):
    """
    Bootstrap the whole thing

    :param argv: list of command line arguments
    """

    # Parse the command line
    args = init_parsecmdline(argv[1:])

    # This baby will handle UNIX signals
    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    # initialize log
    if not args['--log-file']:
        args['--log-file'] = log.LOG_FILE_DEFAULT
    log.init(log_file=args['--log-file'],
             threshold_lvl=int(args['--log-level']))

    # show splash
    _splash()

    # after all has been done, give options that had been
    # gotten from the command line
    return args


def _handle_signal(signum, frame):
    """
    UNIX signal handler
    """
    # Raise a SystemExit exception
    sys.exit(1)


def shutdown():
    """
    Cleanup
    """
    log.msg("Exiting ...")


def _handle_except(e):
    """
    Handle (log) any exception

    :param e: exception to be handled
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    log.msg_err("Unhandled {e} at {file}:{line}: '{msg}'" .format(
        e=exc_type.__name__, file=fname,
        line=exc_tb.tb_lineno, msg=e))
    log.msg_err(traceback.format_exc())
    log.msg_err("An error has occurred!. "
                "For more details, review the logs.")
    return 1


def main(argv=None):
    """
    This is the main thread of execution

    :param argv: list of command line arguments
    """
    # Exit code
    exit_code = 0

    # First, we change main() to take an optional 'argv'
    # argument, which allows us to call it from the interactive
    # Python prompt
    if argv is None:
        argv = sys.argv

    try:
        # Bootstrap
        options = init(argv)

        # ... and proceed to create images from the config file
        if options['--list']:
            softlayer.list_instances(options['<config>'],
                                     dry_run=options['--dry-run'])
        else:
            softlayer.capture_instances(options['<config>'],
                                        dry_run=options['--dry-run'])

    except DocoptExit as dexcept:
        # Deal with wrong arguments
        print(dexcept)
        exit_code = 1
    except Exception as e:
        # ... and if everything else fails
        _handle_except(e)
        exit_code = 1
    finally:
        # All cleanup actions are taken from here
        shutdown()
    return exit_code


# Now the sys.exit() calls are annoying: when main() calls
# sys.exit(), your interactive Python interpreter will exit!.
# The remedy is to let main()'s return value specify the
# exit status.
if __name__ == '__main__':
    sys.exit(main())
