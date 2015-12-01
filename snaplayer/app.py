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
from snaplayer import __version__ as version
from snaplayer import (
    PKG_NAME, PKG_URL
)
from snaplayer import log


def init_parsecmdline(argv=[]):
    """
    Parse arguments from the command line

    :param argv: list of arguments
    """
    # use docopt for this one
    pass


def _splash():
    """Print the splash"""
    splash_title = "{pkg} [{version}] - {url}".format(pkg=PKG_NAME,
                                                      version=version, url=PKG_URL)
    log.to_stdout(splash_title, colorf=log.yellow, bold=True)
    log.to_stdout('-' * len(splash_title), colorf=log.yellow, bold=True)


def init(argv):
    """
    Bootstrap the whole thing

    :param argv: list of command line arguments
    """

    # Parse the command line
    init_parsecmdline(argv[1:])

    # This baby will handle UNIX signals
    signal.signal(signal.SIGINT,  _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)


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
    # Perform cleanup
    log.msg("Exiting ...")


def _handle_except(e):
    """
    Handle (log) any exception

    :param e: exception to be handled
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    log.msg_err("Unhandled {e} at {file}:{line}: '{msg}'"
                .format(e=exc_type.__name__, file=fname,
                        line=exc_tb.tb_lineno,  msg=e))
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
        init(argv)

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
