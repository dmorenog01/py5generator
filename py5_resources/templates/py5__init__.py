"""
py5 code, interface to the Java version of Processing using PyJNIus.

This file is created by the py5generator package. Do not edit!
"""
import sys
from pathlib import Path
import logging
import traceback
import time

import jnius_config
if not jnius_config.vm_running:
    current_classpath = jnius_config.get_classpath()
    base_path = Path(
        getattr(sys, '_MEIPASS', Path(__file__).absolute().parent))
    jnius_config.set_classpath(str(base_path / 'jars' / '*'))
    jnius_config.add_classpath(
        *[p for p in current_classpath if p not in jnius_config.get_classpath()])

from jnius import autoclass, detach  # noqa
from jnius import JavaMultipleMethod, JavaMethod  # noqa
from jnius import PythonJavaClass, java_method  # noqa

logger = logging.getLogger(__name__)


class Py5Methods(PythonJavaClass):
    __javainterfaces__ = ['py5/core/Py5Methods']

    def __init__(self, settings, setup, draw):
        self._functions = dict()
        self._functions['settings'] = settings
        self._functions['setup'] = setup
        self._functions['draw'] = draw

    def set_events(self, **kwargs):
        self._functions.update(kwargs)

    def _stop_error(self, msg):
        exc_type, exc_value, exc_tb = sys.exc_info()
        tbe = traceback.TracebackException(exc_type, exc_value, exc_tb)
        tb = list(tbe.format())
        logger.critical(msg + '\n' + tb[0] + ''.join(tb[2:-1]) + '\n' + tb[-1])
        _py5applet.getSurface().stopThread()

    @java_method('(Ljava/lang/String;[Ljava/lang/Object;)V')
    def run_method(self, method_name, params):
        try:
            if method_name == 'draw':
                _update_vars()
        except Exception as e:
            msg = 'internal error in _update_vars: ' + str(e)
            self._stop_error(msg)
            return

        try:
            if method_name in self._functions:
                self._functions[method_name](*params)
        except Exception as e:
            msg = 'exception running ' + method_name + ': ' + str(e)
            self._stop_error(msg)

        # if method_name == 'exitActual':
        #     detach()


Py5Applet = autoclass('py5.core.Py5Applet',
                      include_protected=False, include_private=False)
_py5applet = Py5Applet()
_py5applet_used = False


# *** PY5 GENERATED STATIC CONSTANTS ***
{0}


# *** PY5 GENERATED DYNAMIC VARIABLES ***
{1}


def _update_vars():
    {2}


# *** PY5 GENERATED FUNCTIONS ***
{3}


# *** PY5 USER FUNCTIONS ***
def run_sketch(py5_methods, block=True):
    # setup new py5applet instance
    global _py5applet_used
    if _py5applet_used:
        raise RuntimeError('you can only run one sketch at a time')

    # configure user implemented methods and run
    _py5applet_used = True
    _py5applet.usePy5Methods(py5_methods)
    Py5Applet.runSketch([''], _py5applet)

    if block:
        surface = _py5applet.getSurface()
        while not surface.isStopped():
            time.sleep(0.25)


def get_py5applet():
    global _py5applet
    return _py5applet


def stop_sketch():
    # stop the sketch from running
    if _py5applet and _py5applet_used and not _py5applet.getSurface().isStopped():
        _py5applet.exit()


def _reset_py5():
    """ attempt to reset the py5 library so a new sketch can be executed.

    Note there are race conditions between this and `stop_sketch`. If you call
    this immediately after `stop_sketch` you will might experience problems.
    """
    global _py5applet
    global _py5applet_used
    _py5applet = Py5Applet()
    _py5applet_used = False
